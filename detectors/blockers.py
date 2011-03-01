def blockresolution(db, cl, nodeid, newvalues):
    ''' If the issue has blockers, don't allow it to be resolved.
    '''
    if nodeid is None:
        blockers = []
    else:
        blockers = cl.get(nodeid, 'blockers')
    blockers = newvalues.get('blockers', blockers)

    # don't do anything if there's no blockers or the status hasn't
    # changed
    if not blockers or not newvalues.has_key('status'):
        return

    # get the resolved state ID
    resolved_id = db.status.lookup('resolved')

    # format the info
    u = db.config.TRACKER_WEB
    s = ', '.join(['<a href="%sissue%s">%s</a>'%(
                    u,id,id) for id in blockers])
    if len(blockers) == 1:
        s = 'issue %s is'%s
    else:
        s = 'issues %s are'%s

    # ok, see if we're trying to resolve
    if newvalues['status'] == resolved_id:
        raise ValueError, "This issue can't be resolved until %s resolved."%s


def resolveblockers(db, cl, nodeid, oldvalues):
    ''' When we resolve an issue that's a blocker, remove it from the
        blockers list of the issue(s) it blocks.
    '''
    newstatus = cl.get(nodeid,'status')

    # no change?
    if oldvalues.get('status', None) == newstatus:
        return

    resolved_id = db.status.lookup('resolved')

    # interesting?
    if newstatus != resolved_id:
        return

    # yes - find all the blocked issues, if any, and remove me from
    # their blockers list
    issues = cl.find(blockers=nodeid)
    for issueid in issues:
        blockers = cl.get(issueid, 'blockers')
        if nodeid in blockers:
            blockers.remove(nodeid)
            cl.set(issueid, blockers=blockers)

def init(db):
    # might, in an obscure situation, happen in a create
    db.issue.audit('create', blockresolution)
    db.issue.audit('set', blockresolution)

    # can only happen on a set
    db.issue.react('set', resolveblockers)
