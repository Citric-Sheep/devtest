def serialize_model(instance, nested=True):
    """Serialize a SQLAlchemy model instance to a dictionary."""
    serialized = {}
    for key in instance.__mapper__.c.keys():
        serialized[key] = getattr(instance, key)

    # Serialize nested objects if requested
    if nested:
        for relationship in instance.__mapper__.relationships:
            related_instance = getattr(instance, relationship.key)
            if related_instance and getattr(related_instance, "__mapper__", None):
                serialized[relationship.key] = serialize_model(related_instance)
            else:
                continue

    return serialized