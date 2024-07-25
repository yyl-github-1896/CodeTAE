# CodeTAE

This is the official code repository for the paper "[Exploiting the Adversarial Example Vulnerability of Transfer Learning of Source Code](https://ieeexplore.ieee.org/abstract/document/10531252)"(TIFS 2024).

State-of-the-art source code classification models exhibit excellent task transferability, in which the source code encoders are first pre-trained on a source domain dataset in a self-supervised manner and then fine-tuned on a supervised downstream dataset. Recent studies reveal that source code models are vulnerable to adversarial examples, which are crafted by applying semantic-preserving transformations that can mislead the prediction of the victim model. While existing research has introduced practical black-box adversarial attacks, these are often designed for transfer-based or query-based scenarios, necessitating access to the victim domain dataset or the query feedback of the victim system. These attack resources are very challenging or expensive to obtain in real-world situations. This paper proposes the cross-domain attack threat model against the transfer learning of source code where the adversary has only access to an open-sourced pre-trained code encoder. To achieve such realistic attacks, this paper designs the Code Transfer learning Adversarial Example (CodeTAE) method. CodeTAE applies various semantic-preserving transformations and utilizes a genetic algorithm to generate powerful identifiers, thereby enhancing the transferability of the generated adversarial examples. Experimental results on three code classification tasks show that the CodeTAE attack can achieve 30% ~ 80% attack success rates under the cross-domain cross-architecture setting. Besides, the generated CodeTAE adversarial examples can be used in adversarial fine-tuning to enhance both the clean accuracy and the robustness of the code model.

![image](https://github.com/yyl-github-1896/CodeTAE/assets/87607661/80eda4e6-c314-4acd-b98b-057347003532)

## Requirements

- Python >= 3.7.11
- torch >= 1.13.1
- numpy >= 1.21.5
- transformers >= 4.30.2
- tree-sitter >= 0.20.1
- pandas >= 1.3.5
- tqdm >= 4.65.0

## Substitute ldentifier Generation

Let's take the example that the surrogate encoder is CodeBERT and the dataset is Authorship-Attribution. The usage is similar for other combinations. First, enter the `dataset` directory:

```
cd ./CodeBERT/Authorship-Attribution/dataset
```

Choose one of the commands in the `scripts.sh` file that generates substitute identifiers (comment out the others), for example:

```
CUDA_VISIBLE_DEVICES=0 python get_substitutes.py \
    --store_path ./data_folder/processed_gcjpy/valid_subs.jsonl \
    --base_model=microsoft/codebert-base-mlm \
    --eval_data_file=./data_folder/processed_gcjpy/valid.txt \
    --block_size 512
```

Note that to achieve good results, both substitute identifiers should be generated (`get_substitutes.py` and `get_substitutes_gan`). The generated substitute identifiers is stored at the location of the hyperparameter `--store_path`.

## Obfuscated Code Insertion

First, enter the `code` directory:

```
cd ./CodeBERT/Authorship-Attribution/code
```

Fine-tuning CodeBERT on the training set as a victim model for our attack. You can also download [our fine-tuned models](https://drive.google.com/file/d/1xbNgBJ3tx6V3sCYm2kSBFPcQNqyOXMKw/view?usp=sharing), `model.bin` is a victim model obtained in our experiment. Select the command corresponding to `#train` from the `scripts.sh` file (comment out the others):

```
#train
python run.py \
    --output_dir=./saved_models/gcjpy \
    --model_type=roberta \
    --config_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --tokenizer_name=roberta-base \
    --number_labels 66 \
    --do_train \
    --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
    --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --epoch 30 \
    --block_size 512 \
    --train_batch_size 16 \
    --eval_batch_size 32 \
    --learning_rate 5e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456
```

The fine-tuned model is saved at the location of the hyperparameter `--output_dir`.

Next we generate the adversarial examples on the test set. Choose one of the commands for generating adversarial examples from the `scripts.sh` file (comment out the others), for example:

```
#attack
CUDA_VISIBLE_DEVICES=0 python attack_ablation_ensemble.py \
    --output_dir=./saved_models/gcjpy \
    --model_type=roberta \
    --config_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --tokenizer_name=roberta-base \
    --number_labels 66 \
    --do_eval \
    --csv_store_path ./attack_gi.csv \
    --language_type python \
    --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
    --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --block_size 512 \
    --train_batch_size 8 \
    --eval_batch_size 32 \
    --evaluate_during_training \
    --num_of_changes 2 \
    --seed 123456
```

The location of the generated adversarial examples is in `attack_ablation_ensemble.py`, for example:

```
./adv_codebert_ensemble.txt
```

Note that if you cannot successfully load a pre-trained model from the network, please download the [cached pre-trained models](https://drive.google.com/file/d/1g92kYH4vS0mUU4dbeeHwWVytp70-tBkO/view?usp=sharing).

## Adversarial Fine-tuning

We use the CodeTAE adversarial examples generated on the training set to fine-tune the victim model to improve the generalization and robustness of the victim model. You can also download [our adversarial fine-tuned models](https://drive.google.com/file/d/1xbNgBJ3tx6V3sCYm2kSBFPcQNqyOXMKw/view?usp=sharing), `model_at.bin` is an enhanced model obtained in our experiment.

## Acknowledgments

Our code refers to:

[attack-pretrain-models-of-code](https://github.com/soarsmu/attack-pretrain-models-of-code)

[CODA](https://github.com/tianzhaotju/coda)

## About us

We are in XJTU-AISEC lab led by [Prof. Chao Shen](https://gr.xjtu.edu.cn/en/web/cshen/home), [Prof. Chenhao Lin](https://gr.xjtu.edu.cn/en/web/linchenhao), [Prof. Zhengyu Zhao](https://zhengyuzhao.github.io/), Prof. Qian Li, and etc. in the School of Cyber Science and Engineering, Xi'an Jiaotong University.

Please contact Yulong Yang at xjtu2018yyl0808@stu.xjtu.edu.cn and Haoran Fan at haoran.fan@stu.xjtu.edu.cn if you have any question on the codes. If you find this repository useful, please consider giving ⭐.
