import actions

class assistantActions:
    actionFunction = {}

    def setAction(self, actionId, actionFunc):
        # if self.actionFunction.get(actionId) == None:
        self.actionFunction[actionId] = actionFunc

    

    def performAction(self, command):
        def actionNotFound():
            actions.talk(text = 'Please say the command again.')
        for actionId in self.actionFunction:
            if actionId in command:
                retFunction = self.actionFunction.get(actionId)
                if retFunction==None:
                    continue
                return retFunction
        return actionNotFound


novaActions = assistantActions()

novaActions.setAction('play', actions.talk)
novaActions.setAction('time', actions.playYtMedia)
novaActions.setAction('tell me about', actions.getCurrentTime)
novaActions.setAction('joke', actions.getInfo)
novaActions.setAction('turn off', actions.joke)




