import time
import os

def main():
    data = os.system("Core.py")
    if data == 1:
        print "[ERROR] Erro nas portas do servidor. Reiniciando servidor em 3 segundos."
        time.sleep(3)
        os.system("cls")
        main()
    elif data in [5,1280]:
        print "[INFO] O servidor foi desligado pelo comando /shutdown."
        raw_input("")
    elif data in [11,2816]:
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  10 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  9 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  8 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  7 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  6 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  5 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  4 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  3 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  2 segundos"
        time.sleep(1)
        print "[ERROR] Erros nas portas do servidor. Reiniciando servidor em  1 segundo"
        time.sleep(1)
        os.system("cls")
        main()
    else:
        print "[ERROR] O servidor caiu. Reiniciando-o em 20 segundos."
        time.sleep(20)
        os.system("cls")
        main()

if __name__=="__main__":
    main()
