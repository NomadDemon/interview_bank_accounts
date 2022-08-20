class BaseQuery:
    model = None

    def get_by_id(self, idx):
        obj = self.model.objects.get(pk=idx)
        return obj

    def get_all(self):
        return self.model.objects.all().order_by("pk")

    def count(self):
        return self.model.objects.count()
