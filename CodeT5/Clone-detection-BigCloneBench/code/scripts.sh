#train
CUDA_VISIBLE_DEVICES=0,1,2,3,4 python run.py \
    --output_dir=./saved_models \
    --model_type=t5 \
    --config_name=Salesforce/codet5-base \
    --model_name_or_path=Salesforce/codet5-base \
    --tokenizer_name=codet5-base \
    --do_train \
    --train_data_file=../dataset/train_sampled.txt \
    --eval_data_file=../dataset/valid_sampled.txt \
    --test_data_file=../dataset/test_sampled.txt \
    --epoch 2 \
    --block_size 512 \
    --train_batch_size 16 \
    --eval_batch_size 32 \
    --learning_rate 5e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=5 python run.py \
#     --output_dir=./saved_models \
#     --model_type=t5 \
#     --config_name=Salesforce/codet5-base \
#     --model_name_or_path=Salesforce/codet5-base \
#     --tokenizer_name=codet5-base \
#     --do_asr \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/valid_sampled.txt \
#     --test_data_file=../dataset/test_sampled_0_500.txt \
#     --adv_data_file=./advs_transfer/adv_t5_ours_ensemble.txt \
#     --epoch 2 \
#     --block_size 512 \
#     --train_batch_size 16 \
#     --eval_batch_size 1 \
#     --learning_rate 5e-5 \
#     --max_grad_norm 1.0 \
#     --evaluate_during_training \
#     --seed 123456


#attack
# CUDA_VISIBLE_DEVICES=5 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models \
#     --model_type=t5 \
#     --config_name=Salesforce/codet5-base \
#     --model_name_or_path=Salesforce/codet5-base \
#     --tokenizer_name=codet5-base \
#     --csv_store_path ./attack_base_result_GA.csv \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/test_sampled_0_500.txt \
#     --test_data_file=../dataset/test_sampled.txt \
#     --block_size 512 \
#     --eval_batch_size 32 \
#     --num_of_changes 2 \
#     --seed 123456