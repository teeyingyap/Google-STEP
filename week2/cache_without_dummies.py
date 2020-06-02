import sys

# Cache is a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library (e.g., collections.OrderedDict).
#       Implement the data structure yourself.

# thought process:
# Using a linked list, then insertion will be O(1)
# But deleting item will become O(n)
# so a linked list alone is not enough
# use a hash table + linked list then?
# hash table that maps items to linked list nodes

class Node:
    def __init__(self, url=None, contents=None):
        self.url = url
        self.contents = contents
        self.prev = None
        self.next = None


class Cache:
    # Initializes the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
    	# validation
    	# Assertions are really messages to the developer and should not be caught by client code
    	# since they indicate a programming error.
    	# Asserts are used to test conditions that should never happen. 
    	# The purpose is to crash early in the case of a corrupt program state.
        assert type(n) == int
        assert n > 0, "n should be larger than 0"
        self.n = n
        self.hashtable = {}
        self.head = None
        self.tail = None


    # Access a page and update the cache so that it stores the most
    # recently accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        # dont do anything if the most recent url is the current url
        if self.hashtable:
            if self.head.url == url:
                return
        # if the key is not in the hash table
        # check whether hash table is full or not
        # if not full, create a new node and insert to the head
        # if full, pop last item
        # cannot use popitem() because you cannot guarantee that it is really stored at the end of the hash table?
        if url not in self.hashtable:
            if len(self.hashtable) == self.n:
                last = self.hashtable.pop(self.tail.url)
                self.tail = last.prev
                last.prev.next = None
                last.prev = None
            node = Node(url, contents)
            # if there is nothing in my linked list
            if self.head == None:
                self.tail = node
            else:
                node.next = self.head
                self.head.prev = node
            self.head = node
            self.hashtable[url] = node

        # else if key is in hash table
        # i want to move that item to the head
        else:
            node = self.hashtable[url]
            if node == self.tail:
                self.tail = node.prev
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
            node.next = self.head
            self.head.prev = node
            self.head = node



      # Return the URLs stored in the cache. The URLs are ordered
      # in the order in which the URLs are mostly recently accessed.
    def get_pages(self):
        node = self.head
        urls = []
        while node != None:
            urls.append(node.url)
            node = node.next
        print(urls)
        return urls


# Does your code pass all test cases? :)
def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)
    # Initially, no page is cached.
    equal(cache.get_pages(), [])
    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    equal(cache.get_pages(), ["a.com"])
    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["b.com", "a.com"])
    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
    cache.access_page("c.com", "CCC")
    equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
    cache.access_page("a.com", "AAA")
    equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
    cache.access_page("a.com", "AAA")
    equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
    print("OK!")

    # A helper function to check if the contents of the two lists is the same.
def equal(list1, list2):
    assert(list1 == list2)
    for i in range(len(list1)):
        assert(list1[i] == list2[i])

if __name__ == "__main__":
    cache_test()
