x = "ddaau laf noi co ay.\ndden moi khi thay buon.\nxin lam on hay noi 1 loi"
for i in range(len(x)):
    if x[i] == ".":
        print(x[:i+1])
        print('xxxxxxxxx')
        print(x[i+1:])
        break