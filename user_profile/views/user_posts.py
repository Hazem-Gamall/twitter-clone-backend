from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from user_profile.models import UserProfile, Mention
from main.permissions import IsOwner
from posts.serializers import PostSerializer, MediaSerializer, CreatePostSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from user_profile.parsers import DictFormParser, DictMultiPartParser
from rest_framework import status
from posts.models import Post
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from main.settings import DEBUG
import regex


class UserPostsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()
    parser_classes = [DictFormParser, DictMultiPartParser, JSONParser]
    serializer_class = PostSerializer

    def list(self, request, posts_user__username):
        username = posts_user__username

        if (
            "with_replies" in request.query_params
            and request.query_params["with_replies"] == "true"
        ):
            posts = (
                self.queryset.get(user__username=username)
                .posts.all()
                .order_by("-creation")
            )
        else:
            posts = (
                self.queryset.get(user__username=username)
                .posts.filter(reply_to__isnull=True)
                .order_by("-creation")
            )
        posts = self.paginate_queryset(posts)
        serialized_posts = self.get_serializer(
            posts,
            many=True,
        ).data
        return Response(serialized_posts)

    def create(self, request, posts_user__username):
        request_data = request.data
        mention_pattern = r"(?<=\s|^)@\w{1,35}(?=\s|$)"

        username = posts_user__username
        resource_user = self.queryset.get(user__username=username)
        self.check_object_permissions(request, resource_user)
        user_posts = resource_user.posts
        media_data = None
        print("media" in request_data)
        if "reply_to" in request_data:
            print("reply_to dict", request_data["reply_to"])
        if "media" in request_data:
            media_data = request_data.pop("media")
            print(media_data)

        post_data = {**request_data, "username": username}
        serialized_post = CreatePostSerializer(data=post_data)
        if serialized_post.is_valid():
            saved_post = serialized_post.save()
            user_posts.add(saved_post)
            for match in regex.finditer(mention_pattern, post_data["text"]):
                mentioned_user = self.queryset.filter(user__username=match.group()[1:])

                if not mentioned_user.exists():
                    continue
                new_mention = Mention(
                    user_profile=mentioned_user[0],
                    post=saved_post,
                    start_index=match.start(),
                    end_index=match.end(),
                )
                new_mention.save()
        else:
            raise ValidationError(serialized_post.errors)
        if media_data:
            deserialized_media = MediaSerializer(
                data={"file": media_data, "post": saved_post.id}
            )
            if deserialized_media.is_valid():
                saved_media = deserialized_media.save()
                print("des med", saved_media)
            else:
                return Response(
                    deserialized_media.errors, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(self.get_serializer(saved_post).data)

    @action(methods=["GET"], detail=False, permission_classes=[IsOwner])
    def timeline(self, request, posts_user__username):
        username = posts_user__username

        try:
            resource_user = self.queryset.get(user__username=username)

            self.check_object_permissions(request, resource_user)
            if "following" not in request.GET:
                print("not following")
                return Response(
                    self.get_serializer(
                        self.paginate_queryset(Post.objects.all()), many=True
                    ).data
                )
            timeline_posts = []
            for following in resource_user.following.all():
                timeline_posts += list(following.user_profile.posts.all())
            timeline_posts.sort(key=lambda post: post.creation, reverse=True)
            timeline_posts = self.paginate_queryset(timeline_posts)

            return Response(self.get_serializer(timeline_posts, many=True).data)
        except ObjectDoesNotExist:
            raise ValidationError({"username": {"Does not match any known users."}})
        except Exception as e:
            raise ValidationError(e)
