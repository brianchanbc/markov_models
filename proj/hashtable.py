from collections.abc import MutableMapping

class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        """constructor for Hashtable

        Args:
            capacity: number of buckets in the hashtable
            default_value: value to return when key is not found
            load_factor: ratio of items to capacity, when exceeded, capacity is increased
            growth_factor: factor by which capacity is increased
        """
        # items (list): data in the hashtable, each element (bucket/key) is a linked list
        self._items = [DoublyLinkedList() for _ in range(capacity)]
        self._capacity = capacity
        self._default_value = default_value
        self._load_factor = load_factor
        self._growth_factor = growth_factor
        self._size = 0

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf

        DO NOT CHANGE THIS FUNCTION
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val

    def __setitem__(self, key, val):
        """sets the value of key to val

        Args:
            key: key to hashtable
            val: value to the key
        """
        # get the hash key/bucket
        hash_key = self._hash(key) % self._capacity
        # traverse the linked list to find the node in the key, not the value
        # as our purpose is to update the value of the node
        node = self._items[hash_key].find(key)
        if node:
            # only if node exists, update the value
            node.val = val
        else:
            # if node does not exist, append the node to the end of the linked list
            self._items[hash_key].append(key, val)
            # increase the size of the hashtable by 1
            self._size += 1
            # Resize the hashtable if the load factor is exceeded and rehash every item
            if len(self) / self._capacity > self._load_factor:
                self._capacity *= self._growth_factor
                new_items = [DoublyLinkedList() for _ in range(self._capacity)]
                for linkedlist in self._items:
                    for item_key, item_val in linkedlist:
                        # rehash every item
                        new_items[self._hash(item_key) % self._capacity].append(item_key, item_val)
                self._items = new_items

    def __getitem__(self, key):
        """returns the value of key

        Args:
            key: key to hashtable

        Returns:
            value of key if key is in hashtable, else default_value
        """
        # find the item in the linked list of the key provided
        item = self._items[self._hash(key) % self._capacity].find(key)
        return item.val if item is not None else self._default_value

    def __delitem__(self, key):
        """deletes key from hashtable

        Args:
            key: key to hashtable
        """
        # delete the item in the linked list of the key provided
        del self._items[self._hash(key) % self._capacity][key]
        self._size -= 1

    def __len__(self):
        """returns the number of items in the hashtable

        Returns:
            size: size of hashtable
        """
        return self._size

    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")
    
    def __repr__(self):
        """representation for the hash table when called

        Returns:
            hash table in string format
        """
        elements = []
        for linkedlist in self._items:
            for item_key, item_val in linkedlist:
                elements.append(f'{repr(item_key)}: {repr(item_val)}')
        return '[' + ', '.join(elements) + ']'
     
class Node:
    # Node class for doubly linked list
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None

class DoublyLinkedList:
    # Doubly linked list class
    def __init__(self):
        # constructor for doubly linked list  
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, key, val):
        """appends a node to the end of the linked list

        Args:
            key: key of the node
            val: value of the node
        """
        new_node = Node(key=key, val=val)
        if self._tail:
            # if the linked list is not empty, set the new node as the tail
            self._tail.next = new_node
            new_node.prev = self._tail
        else:
            # if the linked list is empty, set the new node as the head
            self._head = new_node
        self._tail = new_node
        self._size += 1
    
    def find(self, key):
        """finds a node with the given key

        Args:
            key: key of the node to find

        Returns:
            node with the given key if found, else None
        """
        node = self._head
        while node:
            # traverse the linked list to find the node with the given key
            if node.key == key:
                return node
            node = node.next
        # if node is not found, return None
        return None

    def __contains__(self, key):
        """checks if a node with the given key exists
        
        Args:
            key: key of the node to find
        
        Returns:
            True if node with the given key exists, else False
        """
        return self.find(key) is not None
    
    def __delitem__(self, key):
        """deletes a node with the given key

        Args:
            key: key of the node to delete

        Raises:
            KeyError: if node with the given key does not exist
        """
        node = self._head
        while node:
            # traverse the linked list to find the node with the given key
            # if node is found, delete the node
            if node.key == key:
                if node.prev:
                    node.prev.next = node.next
                else:
                    self._head = node.next
                if node.next:
                    node.next.prev = node.prev
                else:
                    self._tail = node.prev
                self._size -= 1
                return
            node = node.next
        # if node is not found, raise KeyError
        raise KeyError(f'Key not found: {key}')

    def __iter__(self):
        """iterates through the linked list

        Yields:
            key, value of each node in the linked list
        """
        node = self._head
        while node:
            # traverse the linked list and yield the key, value of each node
            yield node.key, node.val
            node = node.next
    
    def __len__(self):
        # returns the size of the linked list
        return self._size

    def __repr__(self):
        """representation for the linked list when called

        Returns:
            linked list in string format
        """
        elements = []
        node = self._head
        while node:
            elements.append(f'({repr(node.key)}, {repr(node.val)})')
            node = node.next
        return '[' + ', '.join(elements) + ']'
