import graphene


class Query(graphene.ObjectType):
    say_hello = graphene.String(name=graphene.String(default_value='Test Driven'))

    @staticmethod
    def resolve_say_hello(parent, info, name):
        return f'Hello {name}'