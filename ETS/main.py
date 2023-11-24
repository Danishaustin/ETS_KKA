from collections import deque

class UlarTangga:
    def __init__(self, size):
        self.size = size
        self.board = {}
        self.buff_positions = set()
        self.debuff_positions = set()

    def set_snake_and_ladder(self, snake_and_ladder):
        self.board.update(snake_and_ladder)

    def set_buff_positions(self, buff_positions):
        self.buff_positions = set(buff_positions)

    def set_debuff_positions(self, debuff_positions):
        self.debuff_positions = set(debuff_positions)

    def move(self, current_position, steps):
        new_position = current_position + steps
        if new_position <= self.size:
            return self.board.get(new_position,new_position)
        else:
            return current_position
    
    def check_debuff(self, current_position, dice_result):
        for i in self.debuff_positions:
            if(current_position < i <= current_position + dice_result):
                return 3
        return 1

    def find_shortest_path(self):
        visited = set()
        queue = deque([(1, 0, 0, [])])
        total_step = 0
        moves_list = []

        while queue:
            current_position, steps, buff, moves = queue.popleft()

            # Memastikan jumlah step paling sedikit
            if current_position == self.size:
                if steps < total_step or total_step == 0:
                    total_step = steps
                    moves_list = moves
            
            # Pengaktifan buff
            if current_position in self.buff_positions:
                buff += 3
            
            if buff > 0:
                i = 13
                buff -= 1
            else:
                i = 7

            # Searching menggunakan BFS
            for dice_result in range(1, i):
                new_position = self.move(current_position, dice_result)
                step_increase = self.check_debuff(current_position, dice_result)
                if new_position not in visited:
                    visited.add(new_position)
                    new_moves = moves + [(new_position, steps + step_increase, dice_result)]
                    queue.append((new_position, steps + step_increase, buff, new_moves))
        
        if total_step != 0:
            return total_step, moves_list

        return -1

def main():
    size_of_board = 30
    game = UlarTangga(size_of_board)

    snakes_and_ladders = {}

    # Input ladder
    ladder_count = int(input("Masukkan jumlah tangga: "))
    for _ in range(ladder_count):
        start = int(input("Masukkan posisi tangga: "))
        end = int(input("Masukkan tujuan tangga: "))

        while end <= start or end > size_of_board:
            print("Invalid input! Tujuan tangga harus lebih tinggi dari posisi tangga dan tidak boleh melebihi ukuran papan.")
            end = int(input("Masukkan tujuan tangga: "))

        snakes_and_ladders[start] = end

    # Input snake
    snake_count = int(input("\nMasukkan jumlah ular: "))
    for _ in range(snake_count):
        start = int(input("Masukkan posisi ular: "))
        end = int(input("Masukkan tujuan ular: "))

        while end >= start or end <= 0:
            print("Invalid input! Tujuan ular harus kurang dari posisi ular dan tidak boleh kurang dari atau sama dengan 0.")
            end = int(input("Masukkan tujuan ular: "))

        snakes_and_ladders[start] = end

    # Input buff
    print("\nTerdapat komponen buff, jika melangkah ke petak buff maka 3 langkah selanjutnya bisa berjalan 1-12 langkah")
    buff_count = int(input("Masukkan Jumlah Buff: "))
    buff_positions = []
    for _ in range(buff_count):
        position1 = int(input("Masukkan posisi buff: "))
        buff_positions.append(position1)

    # Input debuff
    print("\nTerdapat komponen debuff, jika terdapat langkah yang melewati petak debuff maka langkah tersebut dianggap 3 langkah")
    debuff_count = int(input("Masukkan Jumlah Debuff: "))
    debuff_positions = []
    for _ in range(debuff_count):
        position2 = int(input("Masukkan posisi debuff: "))
        debuff_positions.append(position2)

    # Memasukkan input ke dalam set
    game.set_buff_positions(buff_positions)
    game.set_debuff_positions(debuff_positions)
    game.set_snake_and_ladder(snakes_and_ladders)

    # Mencari langkah paling sedikit yang dibutuhkan
    shortest_path, moves = game.find_shortest_path()

    if shortest_path != -1:
        position = 1
        print(f"Langkah paling sedikit: {shortest_path}")
        print("Langkah-langkah:")
        for move in moves:
            position += move[2]
            print(f"Langkah {move[1]}")
            if(position < move[0]):
                print(f"Maju {move[2]} bergerak ke posisi {position} naik dengan tangga ke {move[0]}")
                position = move[0]
            elif(position > move[0]):
                print(f"Maju {move[2]} bergerak ke posisi {position} turun dengan ular ke {move[0]}")
                position = move[0]
            else:
                print(f"Maju {move[2]} bergerak ke posisi {move[0]}")
    else:
        print("Tidak ada jalur yang ditemukan.")

if __name__ == "__main__":
    main()
