#include <string>
#include <iostream>
#include <vector>
#include <list>
#include <functional>
#include "gbdt_prediction.cpp"

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
        const double* toward = &v[0];
        return fun(toward);
      };
    funs.push_back(wrapped);
  }
  return funs;
}

int get_max_index(const std::string& filename) {
  auto infile = std::ifstream(filename); std::string line;
  int maxIndex = 0;
  while (std::getline(infile, line)) {
    std::vector<string> pairs; std::istringstream stream(line); string field;
    while (std::getline(stream, field, ' ') ) {
      pairs.push_back(field);
    }
    for(auto pair : pairs ) {
      if(pair.find(':') != std::string::npos) {
        std::string tmp; vector<string> parse; auto ss = std::istringstream(pair);
        while (std::getline(ss, tmp, ':') ) {
          parse.push_back(tmp);
        }
        int index = std::stoi(parse[0]);
        if( maxIndex < index ) maxIndex = index;
      }
    }
  }
  return maxIndex;
}
std::vector<tuple<double, vector<double>>> data_load(std::string fileName = "./dataset/test", int limit = 50000 ) {
  std::cerr << "search Max Index Size " << endl;
  int maxIndex = get_max_index(fileName);
  std::cerr << "Max Index Size is " << maxIndex << std::endl;

  int count = 0;

  std::cerr << "build dataset to memory... " << std::endl;
  std::vector<std::tuple<double, vector<double>>> contains;
  auto infile = ifstream(fileName); std::string line;
  while (std::getline(infile, line)) {
    count += 1;
    if( count > limit ) break;
    try {
      double answer = 0.0;
      std::vector<double> oneline(maxIndex);
      //cout << "data_load1 " << oneline.size() << endl;
      
      vector<string> pairs; std::istringstream stream(line); string field;
      while (std::getline(stream, field, ' ') ) {
        pairs.push_back(field);
      }
      for(auto pair : pairs ) {
        if(pair.find(':') != std::string::npos) {
          std::string tmp; std::vector<std::string> parse; auto ss = std::istringstream(pair);
          while (std::getline(ss, tmp, ':') ) {
            parse.push_back(tmp);
          }

          int index = std::stoi(parse[0]);
          const double data = std::stod(parse[1]);
          oneline[index] = data;
        }
        if( pair.find(':') == std::string::npos) {
          answer = std::stod(pair);
        }
      }
      contains.push_back( std::make_tuple(answer, oneline) );
    } catch ( std::exception& e ) {
      std::cerr << "Exp::" << e.what() << std::endl;
    }
  }
  std::cerr << "Total Dataset size is " << contains.size() << std::endl;
  return contains;
}
int main() {
  auto funs = wrap_up();
  auto contains = data_load();
  for( auto contain : contains ) {
    std::vector<double> Xs = std::get<1>(contain);
    double answer = std::get<0>(contain);
    std::vector<double> nonlinears;
    std::string nonl = std::to_string(answer) + " ";
    for( auto fun : funs ) { 
      nonlinears.push_back( fun(Xs) );
      nonl += std::to_string( fun(Xs) ) + " ";
    }
    std::cout << nonl << std::endl;
  }
}
