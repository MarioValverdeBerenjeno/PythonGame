import multiprocessing
import performance
import game

def start():
    
    p1 = multiprocessing.Process(target=performance.crear_ventana_mod)
    p2 = multiprocessing.Process(target=game.gameloop)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    start()