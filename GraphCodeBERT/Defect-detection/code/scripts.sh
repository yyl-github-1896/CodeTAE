#train
python run.py \
    --output_dir=./saved_models \
    --model_type=roberta \
    --config_name=microsoft/graphcodebert-base \
    --tokenizer_name=microsoft/graphcodebert-base \
    --model_name_or_path=microsoft/graphcodebert-base \
    --do_train \
    --train_data_file=../preprocess/dataset/train.jsonl \
    --eval_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
    --test_data_file=../preprocess/dataset/test.jsonl \
    --epoch 10 \
    --code_length 384 \
    --data_flow_length 128 \
    --train_batch_size 32 \
    --eval_batch_size 64 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=4 python run.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --config_name=microsoft/graphcodebert-base \
#     --tokenizer_name=microsoft/graphcodebert-base \
#     --model_name_or_path=microsoft/graphcodebert-base \
#     --do_asr \
#     --train_data_file=../preprocess/dataset/train.jsonl \
#     --eval_data_file=../preprocess/dataset/valid.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
#     --adv_data_file=./advs_transfer/adv_t5_ablation_ensemble2.txt \
#     --epoch 5 \
#     --code_length 384 \
#     --data_flow_length 128 \
#     --train_batch_size 32 \
#     --eval_batch_size 1 \
#     --learning_rate 2e-5 \
#     --max_grad_norm 1.0 \
#     --seed 123456



#attack
# CUDA_VISIBLE_DEVICES=4 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/graphcodebert-base \
#     --model_name_or_path=microsoft/graphcodebert-base \
#     --csv_store_path ./attack_no_gi.csv \
#     --base_model=microsoft/graphcodebert-base \
#     --eval_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
#     --eval_data_file_2=../preprocess/dataset/test_subs_gan_0_400.jsonl \
#     --code_length 384 \
#     --data_flow_length 128 \
#     --eval_batch_size 64 \
#     --num_of_changes 2 \
#     --seed 123456