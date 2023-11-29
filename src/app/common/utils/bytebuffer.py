import io


class ByteBuffer(object):
    def __init__(self, chunk_size=io.DEFAULT_BUFFER_SIZE):
        self._chunk_size = chunk_size
        self.empty()

    def __len__(self):
        return len(self._bytes) - self._pos

    def read(self, size=-1):
        part = self.peek(size)
        self._pos += len(part)
        return part

    def peek(self, size=-1):
        if size < 0 or size > len(self):
            size = len(self)

        part = self._bytes[self._pos:self._pos+size]
        return part

    def empty(self):
        self._bytes = b''
        self._pos = 0

    def fill(self, source, size=-1):
        size = size if size >= 0 else self._chunk_size
        size = min(size, self._chunk_size)

        if self._pos != 0:
            self._bytes = self._bytes[self._pos:]
            self._pos = 0

        if hasattr(source, 'read'):
            new_bytes = source.read(size)
        else:
            new_bytes = b''
            for more_bytes in source:
                new_bytes += more_bytes
                if len(new_bytes) >= size:
                    break

        self._bytes += new_bytes
        return len(new_bytes)