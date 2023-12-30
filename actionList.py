import actions

class assistantActions:
    actionFunction = {}

    def setAction(self, actionId, actionFunc):
        # if self.actionFunction.get(actionId) == None:
        self.actionFunction[actionId] = actionFunc

    def performAction(self, command):
        def actionNotFound(ai, command):
            ai.talk(text = 'Please say the command again.')
        for actionId in self.actionFunction:
            if actionId in command:
                retFunction = self.actionFunction.get(actionId)
                if retFunction==None:
                    continue
                return retFunction
        return actionNotFound


novaActions = assistantActions()

novaActions.setAction('play', actions.playYtMedia)
novaActions.setAction('time', actions.getCurrentTime)
novaActions.setAction('tell me about', actions.getInfo )
novaActions.setAction('joke', actions.joke)
# novaActions.setAction('turn off', actions.)




