import radix
import time
import collections


class EmulatedRIB(object):
    """Emulated RIB using a Radix object."""

    def __init__(self):
        self.radix = radix.Radix()
        self.access_time = time.time()

    def set_access_time(self, access_time):
        """Set the new access time."""
        self.access_time = access_time

    def update_data(self, node, value, information_key):
        """Update the information stored in a radix node."""

        if not node.data.get(information_key, None):
            # The node was created

            # The OrderedDict() keeps a consistent order and
            # helps comparing results.
            node.data[information_key] = collections.OrderedDict()

        # The node already exist
        node.data[information_key][value] = self.access_time

    def update(self, prefix, value, information_key):
        """Update the information stored concerning a specific prefix."""

        # Check if the entry exists
        node = self.radix.add(prefix)
        if node:
            self.update_data(node, value, information_key)
        return node
    def delete(self, prefix):
        self.radix.delete(prefix)

    def search_all_containing(self, prefix):
        tmp_node = self.radix.search_covering(prefix)
        if tmp_node is None:
            return []
        else:
            return tmp_node

    def search_exact(self, prefix):
        tmp_node = self.radix.search_exact(prefix)
        return tmp_node

    def nodes(self):
        return self.radix.nodes()

    def prefixes(self):
        return self.radix.prefixes()


import logging

from itertools import chain
from collections import namedtuple, OrderedDict

logger = logging.getLogger(__name__)

InternalMessage = namedtuple("InternalMessage",
                             ["type",
                              "timestamp",
                              "collector",
                              "peer_as", "peer_ip",
                              "prefix", "origin",
                              "as_path"
                              ])


PeerInformation = namedtuple("PeerInformation",
                             ["peer_as", "peer_ip"])
RouteInformation = namedtuple("RouteInformation",
                              ["origin", "data"])

def iter_origin(origin):
    """
    Return a list of ASN according to `origin'.
    """
    if isinstance(origin, int):
        yield origin
    elif origin is not None:
        for asn in origin:
            yield asn

def default_route(update):
    """Function that handles the processing of UPDATEs containing
    the default prefixes (where mask length is lower than 8 bits).
    """

    try:
        _, masklen = update.bgp_message_nlri_prefix, update.bgp_message_nlri_prefix_length
        if int(masklen) < 8:
            for asn in iter_origin(update.origin):
                tmp_announce = OrderedDict([("prefix", '/'.join(update.bgp_message_nlri_prefix, update.bgp_message_nlri_prefix_length)),
                                            ("asn", asn),
                                            ("as_path", update.AS_PATH_AS_SEQUENCE)])
                default_info = OrderedDict([("timestamp", update.timestamp),
                                            ("collector", update.aggregator_as),
                                            ("peer_as", update.peer_as),
                                            ("peer_ip", update.peer_ip),
                                            ("announce", tmp_announce)])
                yield default_info
    except ValueError:
        pass
def get_prefix_len(update):
    try:
      prefix_len = int(update.bgp_message_nlri_prefix_length)
    except:
      prefix_len = 0
    return str(prefix_len)

def format_route(update, num_routes):
    for asn in iter_origin(update.origin):
        prefix_len = get_prefix_len(update)
        try:
          prefix = '/'.join([update.bgp_message_nlri_prefix, prefix_len])
        except:
          prefix = '0.0.0.0/0'
        yield OrderedDict([("timestamp", update.timestamp),
                           ("collector", update.aggregator_as),
                           ("peer_as", update.peer_as),
                           ("peer_ip", update.peer_ip),
                           ("type", update.type),
                           ("prefix", prefix),
                           ("as_path", update.AS_PATH_AS_SEQUENCE),
                           ("asn", asn),
                           ("num_routes", num_routes)])


def route(rib, update, data=None):
    """Function that handles the processing of UPDATEs."""
    prefix_len = get_prefix_len(update)
    # Update the RIB with this route information
    peer_info = PeerInformation(update.peer_as, update.peer_ip)
    route_info = RouteInformation(update.AS_PATH_AS_SEQUENCE[-1], data)
    prefix = None
    try:
      prefix = '/'.join([update.bgp_message_nlri_prefix, prefix_len])
    except:
      prefix = '0.0.0.0/0'
    node = rib.update(prefix, peer_info, route_info)
    return format_route(update, len(node.data))


def format_hijack(update, origin, conflict_prefix, conflict_asn):
    """Prepare and return an ordered dictionary, that could be
    logged or manipulated.
    """

    tmp_conflict_with = OrderedDict([("prefix", conflict_prefix),
                                     ("asn", conflict_asn)])
    prefix_len = get_prefix_len(update)
    try:
      prefix = '/'.join([update.bgp_message_nlri_prefix, prefix_len])
    except:
      prefix = '0.0.0.0/0'
    for asn in iter_origin(origin):
        if update.AS_PATH_AS_SEQUENCE is None:
          
            announce_key = "withdraw"
            tmp_announce = OrderedDict([("type", update.type),
                                        ("prefix", prefix),
                                        ("asn", asn)])
        else:
            announce_key = "announce"
            tmp_announce = OrderedDict([("type", update.type),
                                        ("prefix", prefix),
                                        ("asn", asn),
                                        ("as_path", update.AS_PATH_AS_SEQUENCE)])

        yield OrderedDict([("timestamp", update.timestamp),
                           ("collector", update.aggregator_as),
                           ("peer_as", update.peer_as),
                           ("peer_ip", update.peer_ip),
                           (announce_key, tmp_announce),
                           ("conflict_with", tmp_conflict_with),
                           ("asn", conflict_asn)])


def same_origin(origin1, origin2):
    """
    Return True if these two origins have at least one common ASN.
    """
    if isinstance(origin1, int):
        if isinstance(origin2, int):
            return origin1 == origin2
        return origin1 in origin2
    if isinstance(origin2, int):
        return origin2 in origin1
    return len(set(origin1).intersection(set(origin2))) > 0


def hijack(rib, update):
    """Function that handles the processing of UPDATEs and WITHDRAWs in conflict."""

    # List that holds the messages that will be returned
    messages = []

    # Same prefix (first) then less specific hijacks
    origin = update.AS_PATH_AS_SEQUENCE
    
    # in case of NaN
    try:
      prefix_len = int(update.bgp_message_nlri_prefix_length)
    except:
      prefix_len = 0
    try:
      prefix = '/'.join([update.bgp_message_nlri_prefix, str(prefix_len)])
    except:
      prefix = "0.0.0.0/0"
    for node in rib.search_all_containing(prefix):
        if origin is None:
            # if we process a withdraw, we do not know the originating ASN
            # instead we get it from RouteInformation stored in the RIB
            # as it should always be in the first Radix node returned by
            # search_all_containing.
            ri = node.data.get(PeerInformation(update.peer_as, update.peer_ip))
            if ri is None:
                # if we don't find the originating ASN we cannot process
                # further
                return []
            origin = ri.origin

        # Find conflicting ASN origin
        tmp_origins = set()
        for ri_origin, _ in zip(node.data.keys(), node.data.values()):
            if not same_origin(origin, ri_origin):
                tmp_origins.update(iter_origin(ri_origin))

        for asn in tmp_origins:
            messages.append(format_hijack(update, origin, node.prefix, asn))

    return chain.from_iterable(messages)


def format_withdraw(withdraw, origin, num_routes):
    prefix_len = get_prefix_len(withdraw)
    for asn in iter_origin(origin):
        yield OrderedDict([("timestamp", withdraw.timestamp),
                           ("collector", withdraw.collector),
                           ("peer_as", withdraw.peer_as),
                           ("peer_ip", withdraw.peer_ip),
                           ("type", withdraw.type),
                           ("prefix", '/'.join([withdraw.bgp_message_nlri_prefix, str(prefix_len)])),
                           ("asn", asn),
                           ("num_routes", num_routes)])


def withdraw(rib, withdraw):
    """Function that handles the processing of WITHDRAWs."""

    # Withdrawal of routes
    peer_info = PeerInformation(withdraw.peer_as, withdraw.peer_ip)
    prefix_len = get_prefix_len(withdraw)
    try:
      wprefix = '/'.join([withdraw.bgp_message_nlri_prefix, str(prefix_len)])
    except:
      wprefix = '0.0.0.0/0'
    node = rib.search_exact(wprefix)
    if node is not None:
        ri = node.data.pop(peer_info, None)
        num_routes = len(node.data)
        if num_routes == 0:
            rib.delete(wprefix)
        if ri is not None:
            return format_withdraw(withdraw, ri.origin, num_routes)
    return []

logger = logging.getLogger(__name__)


def process_message(rib, collector, message, is_watched=None, data=None):
    """
    Modify the RIB according to the BGP `message'.
    """
    default = list(default_route(message))
    if len(default) > 0:
        # XXX replace with a filter function
        # we ignore default routes
        return default, [], []

    conflicts = list(hijack(rib, message))
    if message.AS_PATH_AS_SEQUENCE is None or message.AS_PATH_AS_SEQUENCE[-1] is None:
        routes = withdraw(rib, message)
    elif len(conflicts) > 0 \
            or is_watched is None or is_watched(message) is True:
        routes = route(rib, message, data)
    else:
        routes = []
    return default, routes, conflicts

