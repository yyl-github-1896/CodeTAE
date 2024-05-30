#train
CUDA_VISIBLE_DEVICES=0,1,2,3,4 python run.py \
    --output_dir=./saved_models \
    --model_type=t5 \
    --config_name=Salesforce/codet5-base \
    --model_name_or_path=Salesforce/codet5-base \
    --tokenizer_name=codet5-base \
    --do_train \
    --train_data_file=../preprocess/dataset/train.jsonl \
    --eval_data_file=../preprocess/dataset/valid.jsonl \
    --test_data_file=../preprocess/dataset/test.jsonl \
    --epoch 5 \
    --block_size 512 \
    --train_batch_size 24 \
    --eval_batch_size 64 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=4 python run.py \
#     --output_dir=./saved_models \
#     --model_type=t5 \
#     --config_name=Salesforce/codet5-base \
#     --model_name_or_path=Salesforce/codet5-base \
#     --tokenizer_name=codet5-base \
#     --do_asr \
#     --train_data_file=../preprocess/dataset/train.jsonl \
#     --eval_data_file=../preprocess/dataset/valid.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
#     --adv_data_file=./advs_transfer/adv_t5_ablation_ensemble2.txt \
#     --epoch 5 \
#     --block_size 512 \
#     --train_batch_size 24 \
#     --eval_batch_size 1 \
#     --learning_rate 2e-5 \
#     --max_grad_norm 1.0 \
#     --evaluate_during_training \
#     --seed 123456



#attack
# CUDA_VISIBLE_DEVICES=4 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models \
#     --model_type=t5 \
#     --config_name=Salesforce/codet5-base \
#     --model_name_or_path=Salesforce/codet5-base \
#     --tokenizer_name=codet5-base \
#     --csv_store_path ./attack_genetic.csv \
#     --train_data_file=../preprocess/dataset/train_subs.jsonl \
#     --eval_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
#     --eval_data_file_2=../preprocess/dataset/test_subs_gan_0_400.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs.jsonl \
#     --block_size 512 \
#     --eval_batch_size 64 \
#     --num_of_changes 2 \
#     --seed 123456
