#include <string>
#include <iostream>
#include <vector>
#include <list>
#include <functional>
#include "./gbdt_prediction.cpp"

#include <fstream>
#include <sstream>
#include <tuple>
using namespace std;

vector<function<double(const vector<double>&)>> 
wrap_up() {
  auto functions = LightGBM::PredictTreeLeafPtr;
  vector<function<double(const vector<double>&)>> funs;
  for(int i=0; i < 8000; i++ ) {
    std::function<double(const double*)> fun = *functions[i];
    auto wrapped = [fun, i](const vector<double>& v) {
        // change to array
        //cout << "no tree." << i << endl;
        /*for(auto d : v ) {
          cout << d << endl;
        }*/
        
        //cout << "scaned." << v.size() << endl;
        const double* toward = &v[0];
        return fun(toward);
      };
    funs.push_back(wrapped);
  }
  return funs;
}

vector<tuple<double, vector<double>>> data_load() {
  auto infile = ifstream("./dataset/test");
  std::string line;
  cout << "a b 2" << endl;

  vector<std::tuple<double, vector<double>>> contains;
  const int Limit = 10000; 
  int count = 0;
  while (std::getline(infile, line)) {
    count += 1;
    if( count > Limit ) break;
    //cout << line << endl;
    try {
      double anser = 0.0;
      std::vector<double> oneline(300000);
      //cout << "data_load1 " << oneline.size() << endl;
      
      vector<string> pairs; std::istringstream stream(line); string field;
      while (std::getline(stream, field, ' ') ) {
        pairs.push_back(field);
      }
      for(auto pair : pairs ) {
        if(pair.find(':') != std::string::npos) {
          string tmp; vector<string> parse; auto ss = std::istringstream(pair);
          while (std::getline(ss, tmp, ':') ) {
            parse.push_back(tmp);
          }

          int index = stoi(parse[0]);
          const double data = stod(parse[1]);
          oneline[index] = data;
          //cout << pair << endl;
        }
        if( pair.find(':') == std::string::npos) {
          anser = stod(pair);
        }
      }
      //cout << "data_load2 " << oneline.size() << endl;
      contains.push_back( std::make_tuple(anser, oneline) );
    } catch ( std::exception& e ) {
      cout << "Exp::" << e.what() << endl;
    }
  }
  return contains;
}
int main() {
  auto funs = wrap_up();
  auto contains = data_load();
  cout << "size" << contains.size() << endl;
  for( auto contain : contains ) {
    vector<double> Xs = std::get<1>(contain);
    double answer = std::get<0>(contain);
    vector<double> nonlinears;
    string nonl = to_string(answer) + " ";
    for( auto fun : funs ) { 
      nonlinears.push_back( fun(Xs) );
      nonl += to_string( fun(Xs) ) + " ";
    }
    cout << nonl << endl;
  }
}
