[![Build Status](https://travis-ci.org/Matvey-Kuk/P2PFileExchange.png?branch=master)](https://travis-ci.org/Matvey-Kuk/P2PFileExchange)

About:
------------
Distributed absolutely decentralised file storage for workgroups with git-like versioning.

How to run:
------------
python3 Main.py -h

Tests:

cd P2PFileExchange

python3 -m unittest discover --start-directory=Tests --pattern=*.py

CPython interpreter 3.4 required

Commands:
------------

Connection control:

Command  | Description
------------- | -------------
p2p connect_to %ip:port% | Connect to peer.
p2p show_peers | Show connected peers.

Управление личными данными:

Command  | Description
------------- | -------------
auth load_keys %keystorage file% | Auth.
auth register %username%  | Register new user.
auth save_keys %keystorage file% | Save keystorage file.
auth logout | Log out.
auth show_last_connection_time %username%  | Get last user online time by username.

Workgroup control:

Command  | Description
------------- | -------------
auth add_user_to_group %group name% %username%  | Add user to group. Group would be created if not exists.
auth remove_user_from_group %group name% %username%  | Remove user from group.
auth show_users_in_group  %group admin username% %group name%  | Show usernames for all users in group.
auth show_users_groups  %group admin username% | Show all user's groups.
auth work_in_group  %group admin username% %group name% %local dir for group's files%  | Enabale file syncing.
auth stop_working_in_group %group admin username% %group name% | Disable file syncing.
auth show_groups_i_am_working_in | List enabled groups.

Working with files:

Command  | Description
------------- | -------------
files work_with %group admin username% %group name% | Enable group's files editing mode.
files block_files %filename filename filename ...% | Disable syncing for certain files.
files release_blocked_files | Enable syncing for all files.
files leave_working_group | Disable group's files editing mode.
