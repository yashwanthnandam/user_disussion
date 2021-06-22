from django_elasticsearch_dsl import ( Document, fields, Index)

from ..models  import CustomUser, Discussion

PUBLISHER_INDEX = Index('discussion',)

PUBLISHER_INDEX.settings(
    number_of_shards = 1,
    number_of_replicas=1
)

@PUBLISHER_INDEX.doc_type
class discussionDocument(Document):
    id = fields.IntegerField(attr="id")
    text = fields.TextField(
        fields = {
            "raw": {
                "type":'keyword'
            }
        }
    )
    class Django(object):
        model = Discussion
