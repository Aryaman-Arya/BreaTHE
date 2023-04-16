# BreaTHE - Breath Tracking and Health Evaluation

**Project Theme:** Healthcare

**Team :** Aryaman, Yash Ghodekar, Sanjam Kaur Bedi

**BreaTHE** is a web application that uses the **audio clip of a user's breathing pattern** and evaluates their respiratory health. The web app provides insights into the user's respiratory health by checking whether the user falls into any of the following categories: **Bronchiolitis, Pneumonia, URTI, COPD, or Healthy**. BreaTHE has the potential to help people manage their respiratory health, especially in the current global pandemic, where respiratory illnesses are a significant concern to the whole humanity.

We are currently using the **ICBHI, 2017** challenge dataset for model training. The data samples include the respiratory sounds of both healthy individuals, as well as of patients who were having respiratory ailments. The patients span all age groups, including young children, adults, and senior citizens. The dataset consists of a total of **5.5 h of recordings containing 6898 respiratory cycles**, of which 1,864 contain crackles, 886 contain wheezes, and 506 contain both crackles and wheezes, in 920 annotated audio samples from 126 subjects.

The distribution of the Dataset (before augmentation):

![Untitled](https://user-images.githubusercontent.com/75626387/229480543-113d512b-8309-4371-beba-24b1692fac0a.png)

As the number of data samples for some classes in the dataset is too low for training the model, we applied the **data augmentation** on the dataset, which is a technique commonly used in machine learning and computer vision to increase the amount and diversity of data available for training a model. It involves applying various transformations or modifications to existing data samples to create new synthetic data samples that are similar to real-world data. Another pre-processing step was to remove rare diseases like asthma and LRTI, which occurred only among 2 patients.

The distribution of the Dataset (after Augmentation):

![image](https://user-images.githubusercontent.com/85841043/229993755-c4fa7e48-696d-4be2-b34c-1fa880e1eeff.png)

In this project, first, our aim was to **convert the audio file to a visual image**. We achieved that by converting audio files (.wav format) to a **digital spectrogram using MFCC** (mel-frequency cepstrum coefficient).

Auditory signals post data augmentation - 

![image](https://user-images.githubusercontent.com/85841043/230002355-661e0acc-538c-4469-8a76-2138228a86a6.png)

Signals after Log-Mel transform - 

![image](https://user-images.githubusercontent.com/85841043/230003483-d3c861c8-9d30-4fc1-83eb-3ce58d37639f.png)

