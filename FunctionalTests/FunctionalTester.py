from FunctionalTests.Instance import *


instance = Instance('-port 1235 -P2PModule -UsersDatabaseModule -functionalTestInteractionPort 1111')
print(instance.send_command('auth register matvey'))
instance.kill()
