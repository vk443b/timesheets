from graphene_django import DjangoObjectType
import graphene
from users.models import Users

class User(DjangoObjectType):
    class Meta:
        model = Users

class Query(graphene.ObjectType):
    users = graphene.List(User)

    @graphene.resolve_only_args
    def resolve_users(self):
        return Users.objects.all()

schema = graphene.Schema(query=Query)