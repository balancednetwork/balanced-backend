# import random
# import string
#
# from balanced_backend.main_streaming import main
# from balanced_backend.config import settings
#
#
# def test_streaming():
#     settings.CONSUMER_GROUP = ''.join(
#         random.choice(string.ascii_uppercase + string.digits) for _ in range(3)
#     )
#     main()
