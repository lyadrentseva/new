import json
import os


def print_with_indent(value, indent=0):
    print('\t' * indent + f'{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, record):
        self.entries.append(record)
        record.parent = self

    def print_entries(self, ind=0):
        print_with_indent(self, ind)
        for i in self.entries:
            i.print_entries(ind=ind + 1)

    def json(self):
        en = []
        for entry in self.entries:
            en.append(entry.json())
        return {
            "title": self.title,
            "entries": en
        }

    @classmethod
    def from_json(cls, value: dict):
        ex = cls(value['title'])
        for entry in value['entries']:
            ex.add_entry(cls.from_json(entry))
        return ex

    def save(self, path):
        p = os.path.join(path, f'{self.title}.json')
        with open(p, 'w') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return cls.from_json(content)


from typing import List
from resources import Entry
import os


class EntryManager:
    def __init__(self, data_path: str):
        entries = []
        self.data_path = data_path
        self.entries = entries

    def save(self):
        for i in self.entries:
            ex = Entry(f'{i}')
            ex.save(self.data_path)

    def load(self):
        for i in os.listdir(self.data_path):
            if i[-5:] == '.json':
                entry = Entry.load(os.path.join(self.data_path, i))
                self.entries.append(entry)

