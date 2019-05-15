def add_permissions(UserModel, PermissionModel, ContentTypeModel):
    ct = ContentTypeModel.objects.get_for_model(UserModel)
    PermissionModel.objects.create(codename='manage_producers', name='Can manage producers', content_type=ct)
    PermissionModel.objects.create(codename='manage_managers', name='Can manage managers', content_type=ct)
    PermissionModel.objects.create(codename='manage_rex', name='Can manage rex', content_type=ct)
