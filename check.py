# # # a = (1, 2, 3)
# # # b = {email: "rahulsarkar334@gmail.com"}
# # #
# # # print(b.email)
# #
# # from utils.tokenization import encode_token, token_required
# #
# #
# # # x = encode_token(user_id='12345')
# #
# # @token_required
# # def run_auth():
# #     print("Access Granted")
# #
# #
# # print(run_auth())
#
# a = {
#     "name": "Rahul",
#     "age": 28,
#     "location": "BLR"
# }
#
# b = {
#     "name": "Rahul",
#     "age": 28,
#     "location": "LONDON"
# }
#
# shared_items = {k: a[k] for k in a if k in b and a[k] != b[k]}
#
# print(shared_items)
# a =1

# def chel():
#     global a
#     a = 13
# chel()
#
# print(a)


x = [1, 2, 3, 2, 0]
for i in range(0, len(x)):
    print(x[i])
