lambda = 0.1;
num_labels = 3;          % 10 labels, from 1 to 10   
                          % (note that we have mapped "0" to label 10)

m = size(features, 1);

fprintf('\nTraining One-vs-All Logistic Regression...\n')


[all_theta] = oneVsAll(features, labels, num_labels, lambda);

fprintf('Program paused. Press enter to continue.\n');
pause;


%% ================ Part 3: Predict for One-Vs-All ================
%  After ...
pred = predictOneVsAll(all_theta, features);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == labels)) * 100);

