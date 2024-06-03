class MemoryManagementSimulator:
    def __init__(self):
        self.memory = None

    def fixed_size_partitioning(self, memory_size, partition_size, strategy):
        self.memory = FixedSizeMemoryPartitioning(memory_size, partition_size)
        self.run_simulation(strategy)

    def unequal_size_partitioning(self, partitions):
        self.memory = UnequalSizeMemoryPartitioning(partitions)
        self.run_simulation()

    def dynamic_memory_allocation(self, memory_size, strategy):
        self.memory = DynamicMemoryAllocation(memory_size)
        self.run_simulation(strategy)

    def buddy_system(self, size):
        self.memory = BuddySystem(size)
        self.run_simulation()

    def paging(self, memory_size, page_size):
        self.memory = Paging(memory_size, page_size)
        self.run_simulation()

    def run_simulation(self, strategy='first_fit'):
        while True:
            print("\nOptions:\n1. Allocate Memory\n2. Deallocate Memory\n3. Display Memory\n4. Exit")
            choice = input("Enter your choice: ").strip()

            if not choice.isdigit():
                print("Invalid choice, please enter a number.")
                continue

            choice = int(choice)

            if choice == 1:
                process_id = int(input("Enter process ID: "))
                process_size = int(input("Enter process size: "))
                if isinstance(self.memory, Paging):
                    self.memory.allocate_memory(process_id, process_size)
                else:
                    self.memory.allocate_memory(process_id, process_size, strategy)
            elif choice == 2:
                process_id = int(input("Enter process ID to deallocate: "))
                self.memory.deallocate_memory(process_id)
            elif choice == 3:
                self.memory.display_memory()
            elif choice == 4:
                break
            else:
                print("Invalid choice, please try again.")

class FixedSizeMemoryPartitioning:
    def __init__(self, memory_size, partition_size):
        self.memory_size = memory_size
        self.partition_size = partition_size
        self.partitions = [{'size': partition_size, 'occupied': False, 'process': None} for _ in range(memory_size // partition_size)]

    def allocate_memory(self, process_id, process_size, strategy='first_fit'):
        if process_size > self.partition_size:
            print(f"Process {process_id} size {process_size} exceeds partition size {self.partition_size}")
            return False
        
        if strategy == 'first_fit':
            return self.first_fit(process_id, process_size)
        elif strategy == 'best_fit':
            return self.best_fit(process_id, process_size)
        elif strategy == 'worst_fit':
            return self.worst_fit(process_id, process_size)
        else:
            print("Unknown strategy")
            return False

    def first_fit(self, process_id, process_size):
        for partition in self.partitions:
            if not partition['occupied'] and partition['size'] >= process_size:
                partition['occupied'] = True
                partition['process'] = process_id
                return True
        print(f"No suitable partition found for process {process_id} using first fit")
        return False

    def best_fit(self, process_id, process_size):
        best_partition = None
        for partition in self.partitions:
            if not partition['occupied'] and partition['size'] >= process_size:
                if best_partition is None or partition['size'] < best_partition['size']:
                    best_partition = partition
        
        if best_partition:
            best_partition['occupied'] = True
            best_partition['process'] = process_id
            return True
        print(f"No suitable partition found for process {process_id} using best fit")
        return False

    def worst_fit(self, process_id, process_size):
        worst_partition = None
        for partition in self.partitions:
            if not partition['occupied'] and partition['size'] >= process_size:
                if worst_partition is None or partition['size'] > worst_partition['size']:
                    worst_partition = partition
        
        if worst_partition:
            worst_partition['occupied'] = True
            worst_partition['process'] = process_id
            return True
        print(f"No suitable partition found for process {process_id} using worst fit")
        return False

    def deallocate_memory(self, process_id):
        for partition in self.partitions:
            if partition['occupied'] and partition['process'] == process_id:
                partition['occupied'] = False
                partition['process'] = None
                return True
        print(f"Process {process_id} not found in memory")
        return False

    def display_memory(self):
        for i, partition in enumerate(self.partitions):
            print(f"Partition {i}: {'Occupied by process ' + str(partition['process']) if partition['occupied'] else 'Free'}")

class UnequalSizeMemoryPartitioning:
    def __init__(self, partitions):
        self.partitions = [{'size': size, 'occupied': False, 'process': None} for size in partitions]

    def allocate_memory(self, process_id, process_size, strategy=None):
        for partition in self.partitions:
            if not partition['occupied'] and partition['size'] >= process_size:
                partition['occupied'] = True
                partition['process'] = process_id
                return True
        print(f"No suitable partition found for process {process_id}")
        return False

    def deallocate_memory(self, process_id):
        for partition in self.partitions:
            if partition['occupied'] and partition['process'] == process_id:
                partition['occupied'] = False
                partition['process'] = None
                return True
        print(f"Process {process_id} not found in memory")
        return False

    def display_memory(self):
        for i, partition in enumerate(self.partitions):
            print(f"Partition {i}: {'Occupied by process ' + str(partition['process']) if partition['occupied'] else 'Free'}")

class DynamicMemoryAllocation:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.memory = [{'start': 0, 'size': memory_size, 'occupied': False, 'process': None}]

    def allocate_memory(self, process_id, process_size, strategy='first_fit'):
        if strategy == 'first_fit':
            return self.first_fit(process_id, process_size)
        elif strategy == 'best_fit':
            return self.best_fit(process_id, process_size)
        elif strategy == 'worst_fit':
            return self.worst_fit(process_id, process_size)
        else:
            print("Unknown strategy")
            return False

    def first_fit(self, process_id, process_size):
        for block in self.memory:
            if not block['occupied'] and block['size'] >= process_size:
                self.split_block(block, process_id, process_size)
                return True
        print(f"No suitable block found for process {process_id} using first fit")
        return False

    def best_fit(self, process_id, process_size):
        best_block = None
        for block in self.memory:
            if not block['occupied'] and block['size'] >= process_size:
                if best_block is None or block['size'] < best_block['size']:
                    best_block = block
        
        if best_block:
            self.split_block(best_block, process_id, process_size)
            return True
        print(f"No suitable block found for process {process_id} using best fit")
        return False

    def worst_fit(self, process_id, process_size):
        worst_block = None
        for block in self.memory:
            if not block['occupied'] and block['size'] >= process_size:
                if worst_block is None or block['size'] > worst_block['size']:
                    worst_block = block
        
        if worst_block:
            self.split_block(worst_block, process_id, process_size)
            return True
        print(f"No suitable block found for process {process_id} using worst fit")
        return False

    def split_block(self, block, process_id, process_size):
        if block['size'] > process_size:
            new_block = {'start': block['start'] + process_size, 'size': block['size'] - process_size, 'occupied': False, 'process': None}
            self.memory.insert(self.memory.index(block) + 1, new_block)
        block['size'] = process_size
        block['occupied'] = True
        block['process'] = process_id

    def deallocate_memory(self, process_id):
        for block in self.memory:
            if block['occupied'] and block['process'] == process_id:
                block['occupied'] = False
                block['process'] = None
                self.merge_free_blocks()
                return True
        print(f"Process {process_id} not found")
        return False

    def merge_free_blocks(self):
        i = 0
        while i < len(self.memory) - 1:
            if not self.memory[i]['occupied'] and not self.memory[i + 1]['occupied']:
                self.memory[i]['size'] += self.memory[i + 1]['size']
                del self.memory[i + 1]
            else:
                i += 1

    def display_memory(self):
        for block in self.memory:
            print(f"Block {block['start']} - Size: {block['size']}, {'Occupied by process ' + str(block['process']) if block['occupied'] else 'Free'}")

class BuddySystem:
    def __init__(self, size):
        self.size = size
        self.memory = [{'start': 0, 'size': size, 'occupied': False, 'process': None}]

    def allocate_memory(self, process_id, process_size):
        for block in self.memory:
            if not block['occupied'] and block['size'] >= process_size:
                while block['size'] > process_size * 2:
                    self.split_block(block)
                block['occupied'] = True
                block['process'] = process_id
                return True
        print(f"No suitable block found for process {process_id}")
        return False

    def split_block(self, block):
        half_size = block['size'] // 2
        new_block = {'start': block['start'] + half_size, 'size': half_size, 'occupied': False, 'process': None}
        block['size'] = half_size
        self.memory.insert(self.memory.index(block) + 1, new_block)

    def deallocate_memory(self, process_id):
        for block in self.memory:
            if block['occupied'] and block['process'] == process_id:
                block['occupied'] = False
                block['process'] = None
                self.merge_buddies()
                return True
        print(f"Process {process_id} not found")
        return False

    def merge_buddies(self):
        i = 0
        while i < len(self.memory) - 1:
            current_block = self.memory[i]
            next_block = self.memory[i + 1]
            if not current_block['occupied'] and not next_block['occupied'] and current_block['size'] == next_block['size']:
                current_block['size'] *= 2
                del self.memory[i + 1]
            else:
                i += 1

    def display_memory(self):
        for block in self.memory:
            print(f"Block {block['start']} - Size: {block['size']}, {'Occupied by process ' + str(block['process']) if block['occupied'] else 'Free'}")

class Paging:
    def __init__(self, memory_size, page_size):
        self.memory_size = memory_size
        self.page_size = page_size
        self.num_frames = memory_size // page_size
        self.frames = [{'occupied': False, 'process': None, 'page': None} for _ in range(self.num_frames)]
        self.page_tables = {}

    def allocate_memory(self, process_id, process_size):
        num_pages = (process_size + self.page_size - 1) // self.page_size
        if num_pages > self.num_frames - sum(frame['occupied'] for frame in self.frames):
            print(f"Not enough memory for process {process_id}")
            return False
        
        page_table = []
        for i in range(num_pages):
            for frame in self.frames:
                if not frame['occupied']:
                    frame['occupied'] = True
                    frame['process'] = process_id
                    frame['page'] = i
                    page_table.append(frame)
                    break
        self.page_tables[process_id] = page_table
        return True

    def deallocate_memory(self, process_id):
        if process_id in self.page_tables:
            for frame in self.page_tables[process_id]:
                frame['occupied'] = False
                frame['process'] = None
                frame['page'] = None
            del self.page_tables[process_id]
            return True
        print(f"Process {process_id} not found")
        return False

    def display_memory(self):
        for i, frame in enumerate(self.frames):
            print(f"Frame {i}: {'Occupied by process ' + str(frame['process']) + ' page ' + str(frame['page']) if frame['occupied'] else 'Free'}")

def main():
    simulator = MemoryManagementSimulator()

    while True:
        print("\nMemory Management Techniques:\n1. Fixed-sized Memory Partitioning\n2. Unequal-sized Fixed Partitioning\n3. Dynamic Memory Allocation\n4. Buddy System\n5. Paging\n6. Exit")
        choice = input("Select a memory management technique: ").strip()

        if not choice.isdigit():
            print("Invalid choice, please enter a number.")
            continue

        choice = int(choice)

        if choice == 1:
            memory_size = int(input("Enter total memory size: "))
            partition_size = int(input("Enter partition size: "))
            strategy = input("Enter allocation strategy (first_fit, best_fit, worst_fit): ").strip()
            simulator.fixed_size_partitioning(memory_size, partition_size, strategy)
        elif choice == 2:
            partitions = list(map(int, input("Enter partition sizes (comma separated): ").split(',')))
            simulator.unequal_size_partitioning(partitions)
        elif choice == 3:
            memory_size = int(input("Enter total memory size: "))
            strategy = input("Enter allocation strategy (first_fit, best_fit, worst_fit): ").strip()
            simulator.dynamic_memory_allocation(memory_size, strategy)
        elif choice == 4:
            size = int(input("Enter total memory size: "))
            simulator.buddy_system(size)
        elif choice == 5:
            memory_size = int(input("Enter total memory size: "))
            page_size = int(input("Enter page size: "))
            simulator.paging(memory_size, page_size)
        elif choice == 6:
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()