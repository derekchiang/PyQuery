def ServiceHasManyComputeNodes(HasManyRelationship):
  def __init__(self):
    self.parent = models.Service
    self.children = models.ComputeNode

  def queryChildren(attributes):
    services = query(Service).filter(NoopAttribute()).all()
    # Do some magic
    return compute_nodes

relationships += ServiceHasManyComputeNodes()

query(ComputeNode).filter(Attribute('id', EqualTo('123'))).first()

def query(model):
  if isStandalone(model):
    return Query(model)
  else:
    getRelation(model, relations.HAS_MANY).queryChildren(attributes)
