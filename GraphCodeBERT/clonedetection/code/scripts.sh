#train
CUDA_VISIBLE_DEVICES=4,5 python run.py \
    --output_dir=saved_models \
    --config_name=microsoft/graphcodebert-base \
    --model_name_or_path=microsoft/graphcodebert-base \
    --tokenizer_name=microsoft/graphcodebert-base \
    --do_train \
    --train_data_file=../dataset/train_sampled.txt \
    --eval_data_file=../dataset/valid_sampled.txt \
    --test_data_file=../dataset/test_sampled.txt \
    --epoch 2 \
    --code_length 384 \
    --data_flow_length 128 \
    --train_batch_size 14 \
    --eval_batch_size 32 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=5 python run.py \
#     --output_dir=saved_models \
#     --config_name=microsoft/graphcodebert-base \
#     --model_name_or_path=microsoft/graphcodebert-base \
#     --tokenizer_name=microsoft/graphcodebert-base \
#     --do_asr \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/valid_sampled.txt \
#     --test_data_file=../dataset/test_sampled_0_500.txt \
#     --adv_data_file=./advs_transfer/adv_t5_ours_ensemble.txt \
#     --epoch 2 \
#     --code_length 384 \
#     --data_flow_length 128 \
#     --train_batch_size 14 \
#     --eval_batch_size 1 \
#     --learning_rate 2e-5 \
#     --max_grad_norm 1.0 \
#     --evaluate_during_training \
#     --seed 123456


#attack
# CUDA_VISIBLE_DEVICES=4 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --config_name=microsoft/graphcodebert-base \
#     --csv_store_path ./attack_base_result.csv \
#     --model_name_or_path=microsoft/graphcodebert-base \
#     --tokenizer_name=microsoft/graphcodebert-base \
#     --base_model=microsoft/graphcodebert-base \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/test_sampled_0_500.txt \
#     --test_data_file=../dataset/test_sampled.txt \
#     --code_length 384 \
#     --data_flow_length 128 \
#     --eval_batch_size 32 \
#     --num_of_changes 2 \
#     --seed 123456