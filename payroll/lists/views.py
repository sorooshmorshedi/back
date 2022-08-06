class TenderListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.tender"
    serializer_class = TenderSerializer
    filterset_class = TenderFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Tender.objects.hasAccess('get', self.permission_codename).all()
