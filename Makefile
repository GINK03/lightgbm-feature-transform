nonlinearizer: gbdt_prediction.cpp
	clang++ -std=c++1z nonlinearizer.cpp -I/local/include/LightGBM -I./src/boosting -o bin/a.out

.PHONY: clean
clean:
	rm main libsample.so libsample_rust.so
