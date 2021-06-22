from django_elasticsearch_dsl import ( Document, fields, Index)

from ..models import CustomUser

PUBLISHER_INDEX = Index('user',)

PUBLISHER_INDEX.settings(
    number_of_shards = 1,
    number_of_replicas=1
)

@PUBLISHER_INDEX.doc_type
class userDocument(Document):
    id = fields.IntegerField(attr="id")
    first_name = fields.TextField(
        fields = {
            "raw": {
                "type":'keyword'
            }
        }
    )
    class Django(object):
        model = CustomUser
