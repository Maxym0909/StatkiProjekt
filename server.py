import socket
import threading
import pickle
import os

# Get local server IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

HOST = "0.0.0.0"
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print(f"Server running on IP: {get_local_ip()}, port: {PORT}")
print("Waiting for players...")

clients = []
current_player = 0  # 0 for first player, 1 for second
players_ready = 0
game_started = False
lock = threading.Lock()

def broadcast(message):
    for client in clients:
        client.sendall(pickle.dumps(message))

def handle_client(client, opponent, player_id):
    global current_player, players_ready, game_started
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            decoded_data = pickle.loads(data)
            print(f"Received from player {player_id}: {decoded_data}")

            with lock:
                if isinstance(decoded_data, tuple) and decoded_data[0] == "ready":
                    if not game_started:
                        players_ready += 1
                        broadcast(("players_ready", players_ready))
                        if players_ready == 2:
                            game_started = True
                            clients[0].sendall(pickle.dumps("your_turn"))
                            clients[1].sendall(pickle.dumps("wait"))
                            print("Game started!")
                elif isinstance(decoded_data, tuple) and decoded_data[0] == "shot":
                    if game_started and player_id == current_player:
                        opponent.sendall(data)
                    else:
                        client.sendall(pickle.dumps("wait"))
                elif isinstance(decoded_data, tuple) and decoded_data[0] in ["hit", "miss"]:
                    opponent.sendall(data)
                    if decoded_data[0] == "miss":
                        current_player = 1 - current_player
                        client.sendall(pickle.dumps("your_turn"))
                        opponent.sendall(pickle.dumps("wait"))
                    else:
                        opponent.sendall(pickle.dumps("your_turn"))
                        client.sendall(pickle.dumps("wait"))
                elif isinstance(decoded_data, tuple) and decoded_data[0] == "game_over":
                    broadcast(decoded_data)
                    game_started = False
                    players_ready = 0
                    break
    except Exception as e:
        print(f"Error in handle_client: {e}")
    finally:
        client.close()
        with lock:
            if opponent in clients:
                opponent.sendall(pickle.dumps(("opponent_disconnected", None)))
                clients.remove(opponent)
            if client in clients:
                clients.remove(client)
            if not game_started:
                players_ready = 0
        print(f"Player {player_id} disconnected.")

def start_server():
    global players_ready, game_started
    while True:
        try:
            while len(clients) < 2:
                client, addr = server_socket.accept()
                print(f"Player connected: {addr}")
                with lock:
                    clients.append(client)
                    client.sendall(pickle.dumps(("players_ready", players_ready)))
            threading.Thread(target=handle_client, args=(clients[0], clients[1], 0)).start()
            threading.Thread(target=handle_client, args=(clients[1], clients[0], 1)).start()
            while len(clients) > 0:
                pass
            with lock:
                players_ready = 0
                game_started = False
        except KeyboardInterrupt:
            print("Shutting down server...")
            for client in clients:
                client.close()
            server_socket.close()
            break

if __name__ == "__main__":
    start_server()