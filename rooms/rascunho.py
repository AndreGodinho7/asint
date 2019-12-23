def validateCreateSecretariatRequest(createRequest):
    keys = createRequest.keys()
    return "location" in keys and "name" in keys and "description" in keys and "opening_hours" in keys

dict1 = dict(location="lisboa", description="ola", openning_hours="aa")

keys = validateCreateSecretariatRequest(dict1)
print(keys)
print("ola")