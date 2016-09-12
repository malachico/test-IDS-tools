import sys
import test_learning.DNS.aggressive as da
import test_learning.DNS.stealth as ds
import test_learning.DoS.aggressive as oa
import test_learning.DoS.stealth as os
import test_learning.SMTP.aggressive as sa
import test_learning.SMTP.stealth as ss
import test_learning.ICMP.aggressive as ia


def choose_attack(attack):
    print "Chosen attack :", attack

    closure = {
        'da': da.dns_flood,
        'ds': ds.dns_flood,
        'oa': oa.aggressive_dos,
        'os': os.stealth_dos,
        'sa': sa.smtp_flood,
        'ss': ss.smtp_flood,
        'ia': ia.smurf_attack
    }.get(attack, "attack not found")

    # Operate attack closure
    closure()

if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) < 2:
        print "please insert argument from the following: " \
              "DNS aggressive: da" \
              "DNS stealth: ds" \
              "DoS aggressive: oa" \
              "Dos stealth: os" \
              "SMTP aggressive: sa" \
              "SMTP stealth: ss"
        exit(1)

    attack = sys.argv[1]
    choose_attack(attack)
