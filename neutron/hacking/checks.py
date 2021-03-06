# Copyright (c) 2014 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re

import pep8
import six

# Guidelines for writing new hacking checks
#
#  - Use only for Neutron specific tests. OpenStack general tests
#    should be submitted to the common 'hacking' module.
#  - Pick numbers in the range N3xx. Find the current test with
#    the highest allocated number and then pick the next value.
#  - Keep the test method code in the source file ordered based
#    on the N3xx value.
#  - List the new rule in the top level HACKING.rst file
#  - Add test cases for each new rule to
#    neutron/tests/unit/hacking/test_checks.py

_all_log_levels = {
    'reserved': '_',  # this should never be used with a log unless
                      # it is a variable used for a log message and
                      # a exception
    'error': '_LE',
    'info': '_LI',
    'warn': '_LW',
    'warning': '_LW',
    'critical': '_LC',
    'exception': '_LE',
}
_all_hints = set(_all_log_levels.values())
mutable_default_args = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")


def _regex_for_level(level, hint):
    return r".*LOG\.%(level)s\(\s*((%(wrong_hints)s)\(|'|\")" % {
        'level': level,
        'wrong_hints': '|'.join(_all_hints - set([hint])),
    }


log_translation_hint = re.compile(
    '|'.join('(?:%s)' % _regex_for_level(level, hint)
             for level, hint in six.iteritems(_all_log_levels)))

contextlib_nested = re.compile(r"^with (contextlib\.)?nested\(")


def validate_log_translations(logical_line, physical_line, filename):
    # Translations are not required in the test directory
    if "neutron/tests" in filename:
        return
    if pep8.noqa(physical_line):
        return

    msg = "N320: Log messages require translation hints!"
    if log_translation_hint.match(logical_line):
        yield (0, msg)


def use_jsonutils(logical_line, filename):
    msg = "N321: jsonutils.%(fun)s must be used instead of json.%(fun)s"

    # Some files in the tree are not meant to be run from inside Neutron
    # itself, so we should not complain about them not using jsonutils
    json_check_skipped_patterns = [
        "neutron/plugins/ml2/drivers/openvswitch/agent/xenapi/etc/xapi.d/"
        "plugins/netwrap",
    ]

    for pattern in json_check_skipped_patterns:
        if pattern in filename:
            return

    if "json." in logical_line:
        json_funcs = ['dumps(', 'dump(', 'loads(', 'load(']
        for f in json_funcs:
            pos = logical_line.find('json.%s' % f)
            if pos != -1:
                yield (pos, msg % {'fun': f[:-1]})


def no_translate_debug_logs(logical_line, filename):
    """Check for 'LOG.debug(_(' and 'LOG.debug(_Lx('

    As per our translation policy,
    https://wiki.openstack.org/wiki/LoggingStandards#Log_Translation
    we shouldn't translate debug level logs.

    * This check assumes that 'LOG' is a logger.
    N319
    """
    for hint in _all_hints:
        if logical_line.startswith("LOG.debug(%s(" % hint):
            yield(0, "N319 Don't translate debug level logs")


def check_assert_called_once_with(logical_line, filename):
    # Try to detect unintended calls of nonexistent mock methods like:
    #    assert_called_once
    #    assertCalledOnceWith
    #    assert_has_called
    #    called_once_with
    if 'neutron/tests/' in filename:
        if '.assert_called_once_with(' in logical_line:
            return
        uncased_line = logical_line.lower().replace('_', '')

        check_calls = ['.assertcalledonce', '.calledoncewith']
        if any(x for x in check_calls if x in uncased_line):
            msg = ("N322: Possible use of no-op mock method. "
                   "please use assert_called_once_with.")
            yield (0, msg)

        if '.asserthascalled' in uncased_line:
            msg = ("N322: Possible use of no-op mock method. "
                   "please use assert_has_calls.")
            yield (0, msg)


def check_no_contextlib_nested(logical_line, filename):
    msg = ("N324: contextlib.nested is deprecated. With Python 2.7 and later "
           "the with-statement supports multiple nested objects. See https://"
           "docs.python.org/2/library/contextlib.html#contextlib.nested for "
           "more information.")

    if contextlib_nested.match(logical_line):
        yield(0, msg)


def check_python3_xrange(logical_line):
    if re.search(r"\bxrange\s*\(", logical_line):
        yield(0, "N325: Do not use xrange. Use range, or six.moves.range for "
                 "large loops.")


def check_no_basestring(logical_line):
    if re.search(r"\bbasestring\b", logical_line):
        msg = ("N326: basestring is not Python3-compatible, use "
               "six.string_types instead.")
        yield(0, msg)


def check_python3_no_iteritems(logical_line):
    if re.search(r".*\.iteritems\(\)", logical_line):
        msg = ("N327: Use six.iteritems() instead of dict.iteritems().")
        yield(0, msg)


def check_asserttrue(logical_line, filename):
    if 'neutron/tests/' in filename:
        if re.search(r"assertEqual\(\s*True,[^,]*(,[^,]*)?\)", logical_line):
            msg = ("N328: Use assertTrue(observed) instead of "
                   "assertEqual(True, observed)")
            yield (0, msg)
        if re.search(r"assertEqual\([^,]*,\s*True(,[^,]*)?\)", logical_line):
            msg = ("N328: Use assertTrue(observed) instead of "
                   "assertEqual(True, observed)")
            yield (0, msg)


def no_mutable_default_args(logical_line):
    msg = "N329: Method's default argument shouldn't be mutable!"
    if mutable_default_args.match(logical_line):
        yield (0, msg)


def check_assertfalse(logical_line, filename):
    if 'neutron/tests/' in filename:
        if re.search(r"assertEqual\(\s*False,[^,]*(,[^,]*)?\)", logical_line):
            msg = ("N328: Use assertFalse(observed) instead of "
                   "assertEqual(False, observed)")
            yield (0, msg)
        if re.search(r"assertEqual\([^,]*,\s*False(,[^,]*)?\)", logical_line):
            msg = ("N328: Use assertFalse(observed) instead of "
                   "assertEqual(False, observed)")
            yield (0, msg)


def check_assertempty(logical_line, filename):
    if 'neutron/tests/' in filename:
        msg = ("N330: Use assertEqual(*empty*, observed) instead of "
               "assertEqual(observed, *empty*). *empty* contains "
               "{}, [], (), set(), '', \"\"")
        empties = r"(\[\s*\]|\{\s*\}|\(\s*\)|set\(\s*\)|'\s*'|\"\s*\")"
        reg = r"assertEqual\(([^,]*,\s*)+?%s\)\s*$" % empties
        if re.search(reg, logical_line):
            yield (0, msg)


def check_assertisinstance(logical_line, filename):
    if 'neutron/tests/' in filename:
        if re.search(r"assertTrue\(\s*isinstance\(\s*[^,]*,\s*[^,]*\)\)",
                     logical_line):
            msg = ("N331: Use assertIsInstance(observed, type) instead "
                   "of assertTrue(isinstance(observed, type))")
            yield (0, msg)


def check_assertequal_for_httpcode(logical_line, filename):
    msg = ("N332: Use assertEqual(expected_http_code, observed_http_code) "
           "instead of assertEqual(observed_http_code, expected_http_code)")
    if 'neutron/tests/' in filename:
        if re.search(r"assertEqual\(\s*[^,]*,[^,]*HTTP[^\.]*\.code\s*\)",
                     logical_line):
            yield (0, msg)


def factory(register):
    register(validate_log_translations)
    register(use_jsonutils)
    register(check_assert_called_once_with)
    register(no_translate_debug_logs)
    register(check_no_contextlib_nested)
    register(check_python3_xrange)
    register(check_no_basestring)
    register(check_python3_no_iteritems)
    register(check_asserttrue)
    register(no_mutable_default_args)
    register(check_assertfalse)
    register(check_assertempty)
    register(check_assertisinstance)
    register(check_assertequal_for_httpcode)
