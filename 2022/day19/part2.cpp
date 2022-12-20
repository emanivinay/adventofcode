#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <queue>

using namespace std;

struct Blueprint {
    int id;
    int orc, crc, brc1, brc2, grc1, grc2;

    Blueprint(int _id, int _orc, int _crc, int _brc1, int _brc2, int _grc1, int _grc2)
    {
        id = _id;
        orc = _orc;
        crc = _crc;
        brc1 = _brc1;
        brc2 = _brc2;
        grc1 = _grc1;
        grc2 = _grc2;
    }

    Blueprint() {

    };
};

Blueprint* curprint2;


void add(int& o, int& c, int& b, int& g, int orr, int crr, int brr, int grr)
{
    o += orr;
    c += crr;
    b += brr;
    g += grr;
}

string order(64, 'O');
int sz = 0;

pair<int, int> simulate(int T)
{
    // mfg_seq = 'OCBG'
    int t = 0, o = 0, c = 0, b = 0, g = 0, orr = 1, crr = 0, brr = 0, grr = 0;
    int i = 0;
    for (int t = 0;t < T; t++) {
        if (i == sz) {
            // no more making new bots
           add(o, c, b, g, orr, crr, brr, grr);
           continue;
        }

        if (order[i] == 'A') {
            if (o >= curprint2->orc) {
                o -= curprint2->orc;
                orr++;
                o--;
                i++;
            }
        }
        else if (order[i] == 'B') {
            if (o >= curprint2->crc) {
                o -= curprint2->crc;
                crr++;
                c--;
                i++;
            }
        }
        else if (order[i] == 'C') {
            if (o >= curprint2->brc1 && c >= curprint2->brc2) {
                o -= curprint2->brc1;
                c -= curprint2->brc2;
                brr++;
                b--;
                i++;
            }
        }
        else if (order[i] == 'D') {
            if (o >= curprint2->grc1 && b >= curprint2->grc2) {
                o -= curprint2->grc1;
                b -= curprint2->grc2;
                grr++;
                g--;
                i++;
            }
        }

        add(o, c, b, g, orr, crr, brr, grr);
    }

    return {g, i};
}

long long fac(int c)
{
    long long ret = 1;
    for (int i = 1;i <= c; i++) ret *= i;
    return ret;
}

long long total_perms(vector<int> counts)
{
    int total = 0;
    long long denom = 1;
    for (int c : counts) {
        denom *= fac(max(c, 0));
        total += max(c, 0);
    }

    return fac(total) / denom;
}

string get_perm(long long x, int o, int c, int b, int g)
{
    string ret = "";
    int cnts[4] = {o, c, b, g};
    while (cnts[0] + cnts[1] + cnts[2] + cnts[3] > 0) {
        long long total = 0;
        for (char cc : "ABCD") {
            cnts[cc - 'A']--;
            total += total_perms({cnts[0], cnts[1], cnts[2], cnts[3]});
            if (x < total) {
                ret.push_back(cc);
                break;
            }
            cnts[cc - 'A']++;
        }
    }

    return ret;
}

map<pair<int, int>, int> dp;

int recurse(int T, int o, int c, int b, int om, int cm, int bm)
{
    if (T <= 1 ) {
        return 0;
    }

    pair<int, int> key {o * 500 * 500 + c * 500 + b, T * 35 * 35 * 35 + om * 35 * 35 + cm * 35 + bm};
    if (dp.count(key))
        return dp[key];

    int ret = 0;
    if (o >= curprint2->grc1 && b >= curprint2->grc2) {
        ret = max(ret, (T - 1) + recurse(T - 1, o - curprint2->grc1 + om, c + cm, b + bm - curprint2->grc2, om, cm, bm));
        return dp[key] = ret;
    }

    if (o >= curprint2->brc1 && c >= curprint2->brc2) {
        ret = max(ret, recurse(T - 1, o - curprint2->brc1 + om, c - curprint2->brc2 + cm, b + bm, om, cm, bm + 1));
        return dp[key] = ret;
    }
    if (o >= curprint2->orc) {
        ret = max(ret, recurse(T - 1, o - curprint2->orc + om, c + cm, b + bm, om + 1, cm, bm));
    }
    ret = max(ret, recurse(T - 1, o + om, c + cm, b + bm, om, cm, bm));

    if (o >= curprint2->crc) {
        ret = max(ret, recurse(T - 1, o - curprint2->crc + om, c + cm, b + bm, om, cm + 1, bm));
    }

    return dp[key] = ret;
}

int main()
{
    int ret = 0;
    for (int i = 0;i < 3; i++) {
        int id, orc, crc, brc1, brc2, grc1, grc2;
        cin >> id >> orc >> crc >> brc1 >> brc2 >> grc1 >> grc2;
        curprint2 = new Blueprint(id, orc, crc, brc1, brc2, grc1, grc2);

        cout << id << endl;
        dp.clear();
        cout << recurse(32, 0, 0, 0, 1, 0, 0) << endl;
    }

    cout << ret << endl;
    return 0;
}