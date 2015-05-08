import os.path
import logging
from pybloom import BloomFilter


log = logging.getLogger('passcheck.passcheck')
pw_file = os.path.join(os.path.dirname(__file__),
                       'password-files',
                       'common-10k-ascii.txt')
log.debug('Default password file: %s' % pw_file)


class PassCheck(object):

    def __init__(self, password_file=pw_file, fp_rate=0.001, ignore_case=True):
        self._log = logging.getLogger('passcheck.passcheck.PassCheck')
        self._fp_rate = fp_rate
        self._pw_file = os.path.realpath(password_file)
        self._ignore_case = ignore_case
        self._log.debug('Counting items in password file')
        with open(self._pw_file, 'r') as f:
            for line_num, line in enumerate(f):
                pass
        self._num_passwords = line_num + 1
        self._log.debug('Creating BloomFilter with capacity=%d'
                        % self._num_passwords)
        self._bf = BloomFilter(capacity=self._num_passwords,
                               error_rate=self._fp_rate)
        self._log.debug('Loading passwords into BloomFilter')
        num_added = 0
        with open(self._pw_file, 'r') as f:
            for line in f:
                pw = line[:-1]
                if self._ignore_case:
                    pw = pw.lower()
                if not self._bf.add(pw):
                    num_added += 1
                if num_added > self._num_passwords:
                    e = Exception('Password file was modified during load')
                    self._log.error(e)
                    raise e
        # Handle possibility of duplicates (especially if case is ignored)
        if num_added < self._num_passwords:
            self._log.warn('Expected %d passwords, but added %d'
                           % (self._num_passwords, num_added))
            self._num_passwords = num_added

    @property
    def false_positive_rate(self):
        return self._fp_rate

    @property
    def password_file(self):
        return self._pw_file

    @property
    def ignore_case(self):
        return self._ignore_case

    @property
    def num_passwords(self):
        return self._num_passwords

    def __contains__(self, password):
        if self._ignore_case:
            password = password.lower()
        found = password in self._bf
        self._log.debug('Filter contains "%s": %s' % (password, found))
        return found

    def __str__(self):
        return ('[PassCheck: {'
                'num_passwords: %d, '
                'fp_rate: %f, '
                'ignore_case: %s, '
                'password_file: %s}]'
                % (self.num_passwords,
                   self.false_positive_rate,
                   self.ignore_case,
                   self.password_file))
