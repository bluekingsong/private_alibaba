all: train predict

train: lbfgs_interface.cpp common.h linear_search.cpp linear_search.h read_problem.cpp vec_op.cpp vec_op.h als.cpp train.cpp
	g++  als.cpp lbfgs_interface.cpp linear_search.cpp read_problem.cpp vec_op.cpp train.cpp -o train
predict: lbfgs_interface.cpp common.h linear_search.cpp linear_search.h read_problem.cpp vec_op.cpp vec_op.h als.cpp predict.cpp common.cpp
	g++ als.cpp lbfgs_interface.cpp linear_search.cpp read_problem.cpp vec_op.cpp predict.cpp common.cpp -o predict

