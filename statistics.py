import json

from multiprocessing import Pool, current_process, Queue

from Game import ConnectFour
from minmax import minmax
from mcts import mcts


def playSimulation(algorithm1, algorithm2):
    game = ConnectFour()
    while True:
        if game.isBoardFull():
            break

        if game.currentPlayer == 'X':
            if algorithm1[0] == "mcts":
                column = mcts(game, algorithm1[1])
            else:
                column = minmax(game, algorithm1[1], game.currentPlayer)
        else:
            if algorithm2[0] == "mcts":
                column = mcts(game, algorithm2[1])
            else:
                column = minmax(game, algorithm2[1], game.currentPlayer)
        if (not game.isAPossibleMove(column)):
            continue

        game.makeMove(column)
        game.printBoard()

        if game.isWin(column):
            read_write_json('data.json', algorithm1,
                            algorithm2, game.currentPlayer)
            break


def read_write_json(file_path, algorithm1, algorithm2, looser):
    with open(file_path, 'r') as f:
        data = json.load(f)

    simulation_found = False
    for sim in data:
        if data[sim]["X"]["setting"] == algorithm1[1] and data[sim]["X"]["algo"] == algorithm1[0] and data[sim]["O"]["setting"] == algorithm2[1] and data[sim]["O"]["algo"] == algorithm2[0]:
            print(f"Existing simulation found: {sim}")
            simulation_found = True
            simulation_num = sim.split(" ")[-1]
            break

    if not simulation_found:
        simulation_num = len(data) + 1
        data[f"simulation {simulation_num}"] = {
            "total": 0,
            "X": {
                "algo": algorithm1[0],
                "setting": algorithm1[1],
                "lose": 0
            },
            "O": {
                "algo": algorithm2[0],
                "setting": algorithm2[1],
                "lose": 0
            }
        }

    data[f"simulation {simulation_num}"][looser]["lose"] += 1
    data[f"simulation {simulation_num}"]["total"] += 1

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def runSimulations(settings):
    algorithm1, algorithm2 = settings
    gpu_id = queue.get()
    try:
        # run processing on GPU <gpu_id>
        ident = current_process().ident
        print('{}: starting process on GPU {}'.format(ident, gpu_id))
        playSimulation(algorithm1, algorithm2)
        print('{}: finished'.format(ident))
    finally:
        queue.put(gpu_id)


if __name__ == "__main__":
    max_depth = 6
    time = 10
    toRun = toRun = [[["mcts", time], ["minmax", depth]] for _ in range(
        10) for depth in range(1, max_depth)] + [[["minmax", depth], ["mcts", time]] for _ in range(10) for depth in range(1, max_depth)]

    NUM_GPUS = 2
    PROC_PER_GPU = 12

    queue = Queue()

    # initialize the queue with the GPU ids
    for gpu_ids in range(NUM_GPUS):
        for _ in range(PROC_PER_GPU):
            queue.put(gpu_ids)

    pool = Pool(processes=PROC_PER_GPU * NUM_GPUS)
    for _ in pool.imap_unordered(runSimulations, toRun):
        pass
    pool.close()
    pool.join()
