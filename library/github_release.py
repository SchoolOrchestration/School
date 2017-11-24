#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: github_release
short_description: Interact with GitHub Releases
description:
    - Fetch metadata about GitHub Releases
version_added: 2.2
options:
    token:
        description:
            - GitHub Personal Access Token for authenticating
        default: null
    user:
        required: true
        description:
            - The GitHub account that owns the repository
        default: null
    password:
        description:
            - The GitHub account password for the user
        default: null
        version_added: "2.4"
    repo:
        required: true
        description:
            - Repository name
        default: null
    action:
        required: true
        description:
            - Action to perform
        choices: [ 'latest_release', 'create_release' ]
    tag:
        required: false
        description:
            - Tag name when creating a release. Required when using action is set to C(create_release).
        version_added: 2.4
    target:
        required: false
        description:
            - Target of release when creating a release
        version_added: 2.4
    name:
        required: false
        description:
            - Name of release when creating a release
        version_added: 2.4
    body:
        required: false
        description:
            - Description of the release when creating a release
        version_added: 2.4
    draft:
        required: false
        description:
            - Sets if the release is a draft or not. (boolean)
        default: false
        version_added: 2.4
        choices: ['True', 'False']
    prerelease:
        required: false
        description:
            - Sets if the release is a prerelease or not. (boolean)
        default: false
        version_added: 2.4
        choices: ['True', 'False']


author:
    - "Adrian Moisey (@adrianmoisey)"
requirements:
    - "github3.py >= 1.0.0a3"
'''

EXAMPLES = '''
- name: Get latest release of testuseer/testrepo
  github_release:
    token: tokenabc1234567890
    user: testuser
    repo: testrepo
    action: latest_release

- name: Get latest release of test repo using username and password. Ansible 2.4.
  github_release:
    user: testuser
    password: secret123
    repo: testrepo
    action: latest_release

- name: Create a new release
  github:
    token: tokenabc1234567890
    user: testuser
    repo: testrepo
    action: create_release
    tag: test
    target: master
    name: My Release
    body: Some description

'''

RETURN = '''
latest_release:
    description: Version of the latest release
    type: string
    returned: success
    sample: 1.1.0
'''

RELEASE_SHORTCUTS = ['major', 'minor', 'patch']

try:
    import github3
    HAS_GITHUB_API = True
except ImportError:
    HAS_GITHUB_API = False
from ansible.module_utils.basic import AnsibleModule, get_exception

def get_repository(gh_obj, user, repo):
    repo_explicitly_defined = len(repo.split('/')) == 2
    if repo_explicitly_defined:
        user_part, repo_part = repo.split('/')
        return gh_obj.repository(user_part, repo_part)
    else:
        return gh_obj.repository(user, repo)

def validate_release_format(latest_release):
    # todo:
    pass

def bump_version(latest_release, bump):
    if isinstance(latest_release, github3.null.NullObject):
        latest_tag = '0.0.0'
    else:
        latest_tag = latest_release.tag_name

    # todo: handle non semver releases
    tag_index = RELEASE_SHORTCUTS.index(bump)
    major_minor_patch = latest_tag.split('.')
    major_minor_patch[tag_index] = str(int(major_minor_patch[tag_index]) + 1)
    new_release = major_minor_patch[0:(tag_index+1)] + ['0' for x in major_minor_patch[(tag_index+1):]]
    return ".".join(new_release)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            repo=dict(required=True),
            user=dict(required=True),
            password=dict(no_log=True),
            token=dict(no_log=True),
            action=dict(
                required=True, choices=['latest_release', 'create_release']),
            tag=dict(type='str'),
            target=dict(type='str'),
            name=dict(type='str'),
            body=dict(type='str'),
            draft=dict(type='bool', default=False),
            prerelease=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
        required_one_of=(('password', 'token'),),
        mutually_exclusive=(('password', 'token'),),
        required_if=[('action', 'create_release', ['tag'])],
    )

    if not HAS_GITHUB_API:
        module.fail_json(msg='Missing required github3 module (check docs or '
                             'install with: pip install github3.py==1.0.0a4)')

    repo = module.params['repo']
    user = module.params['user']
    password = module.params['password']
    login_token = module.params['token']
    action = module.params['action']
    tag = module.params.get('tag')
    target = module.params.get('target')
    name = module.params.get('name')
    body = module.params.get('body')
    draft = module.params.get('draft')
    prerelease = module.params.get('prerelease')

    # login to github
    try:
        if user and password:
            gh_obj = github3.login(user, password=password)
        elif login_token:
            gh_obj = github3.login(token=login_token)

        # test if we're actually logged in
        gh_obj.me()
    except github3.AuthenticationFailed:
        e = get_exception()
        module.fail_json(msg='Failed to connect to GitHub: %s' % e,
                         details="Please check username and password or token "
                                 "for repository %s" % repo)

    repository = get_repository(gh_obj, user, repo)

    if not repository:
        module.fail_json(msg="Repository %s/%s doesn't exist" % (user, repo))

    if action == 'latest_release':
        release = repository.latest_release()
        if release:
            module.exit_json(tag=release.tag_name)
        else:
            module.exit_json(tag=None)

    if action == 'create_release':
        release_exists = repository.release_from_tag(tag)
        if release_exists:
            module.exit_json(
                skipped=True, msg="Release for tag %s already exists." % tag)

        if tag in RELEASE_SHORTCUTS:
            latest_release = repository.latest_release()
            validate_release_format(latest_release)
            tag = bump_version(latest_release, tag)

        release = repository.create_release(
            tag, target, name, body, draft, prerelease)
        if release:
            module.exit_json(tag=release.tag_name)
        else:
            module.exit_json(tag=None)


if __name__ == '__main__':
    main()