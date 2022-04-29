from graphene import ObjectType, Int, Field
from graphene_federation import build_schema, extend, external, requires

"""
Alphabet order - matters
Y should be just after X in sdl
https://github.com/preply/graphene-federation/issues/26#issuecomment-572127271
"""


@extend(fields="id")
class User(ObjectType):
    id = external(Int(required=True))


@extend(fields="id")
class Article(ObjectType):
    id = external(Int(required=True))
    author = external(Field(lambda: User))
    foo = requires(Int(required=True), fields="id author{id}")

    def resolve_foo(self, info, **kwargs):
        print(self.__dict__, str(info), kwargs)
        return self.author.id

    def __resolve_reference(self, info, **kwargs):
        return Article(
            id=self.id,
        )


class X(ObjectType):
    x_article = Field(Article)


class Y(ObjectType):
    id = Int(required=True)


class Query(ObjectType):
    x = Field(X)
    y = Field(Y)


schema = build_schema(query=Query)
