# Child Malnutrition Risk Assessment App: On-Device ML with TensorFlow Lite & Flutter

An offline-first mobile application designed for real-time child malnutrition risk assessment using local machine learning inference powered by **TensorFlow Lite** and **Flutter**.

---

## Table of Contents
- [What is TensorFlow Lite?](#what-is-tensorflow-lite)
- [How Offline Prediction Works](#how-offline-prediction-works)
- [TensorFlow Lite Workflow](#tensorflow-lite-workflow)
- [Flutter Integration Concept](#flutter-integration-concept)
- [API-Based vs. On-Device Inference](#api-based-vs-on-device-inference)
- [Advantages and Limitations](#advantages-and-limitations)
- [Child Malnutrition Application Use Case](#child-malnutrition-application-use-case)

---

## What is TensorFlow Lite?

**TensorFlow Lite (TFLite)** is an open-source, lightweight cross-platform machine learning framework designed by Google for running inference on mobile, embedded, and edge devices.

Instead of sending user data over the internet to a cloud server to run predictions, TensorFlow Lite enables machine learning models to run directly on local mobile hardware (CPU, GPU, or Neural Processing Units).

---

## How Offline Prediction Works

Offline prediction allows a mobile app to generate AI predictions without an active Wi-Fi or cellular network connection.

1. **Local Asset Storage:** The trained machine learning model is compiled into a lightweight `.tflite` flatbuffer file and bundled inside the mobile app package.
2. **On-Device Preprocessing:** When a user inputs data into the app, the mobile processor normalizes and formats the inputs locally into mathematical tensors.
3. **Local Inference Execution:** The TFLite interpreter loads the model weights into device memory and processes the input tensors directly on the phone's hardware.
4. **Instant Prediction:** The output is calculated and displayed on screen in milliseconds without sending any data over the internet.

```
+-------------------------------------------------------------------+
|                        Mobile Device                              |
|                                                                     |
|  [ User Input ] ---> [ Local Preprocessing ]                      |
|                              |                                    |
|                              v                                    |
|  [ Display Result ] <--- [ TFLite Local Inference Engine ]        |
|                               ^                                   |
|                               |                                   |
|                     [ bundled .tflite Asset ]                     |
+-------------------------------------------------------------------+
```

---

## TensorFlow Lite Workflow

The full pipeline from raw dataset to mobile app deployment follows six core steps:

1. **Dataset Collection & Cleaning:** Gather child demographic and anthropometric records (age, height, weight, MUAC, etc.) and handle missing values.
2. **Model Training (Python):** Train a classification model (e.g., Neural Network, Random Forest, or XGBoost) using TensorFlow, Keras, or Scikit-learn.
3. **Model Evaluation:** Validate model performance on test metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC).
4. **TFLite Model Conversion:** Export the Python model to the `.tflite` format using `tf.lite.TFLiteConverter`. Apply quantization (float16/int8) to compress file size and speed up execution.
5. **Flutter App Integration:** Bundle the `.tflite` model file into the Flutter project's `assets/` directory and configure the `tflite_flutter` package.
6. **On-Device Inference:** Capture user input via Flutter UI, format input tensors, execute prediction locally, and display risk categories to the user.

---

## Flutter Integration Concept

Flutter connects to the TensorFlow Lite C++ runtime using the `tflite_flutter` package via Dart FFI (Foreign Function Interface).

### Core Steps in Dart

1. **Register Asset (`pubspec.yaml`):**

   ```yaml
   flutter:
     assets:
       - assets/models/malnutrition_model.tflite
   ```

2. **Load Model Interpreter:**

   ```dart
   final interpreter = await Interpreter.fromAsset('assets/models/malnutrition_model.tflite');
   ```

3. **Format Inputs:** Convert user inputs into a structured array and apply the same normalization parameters used during model training.

   ```dart
   var inputTensor = [[normAge, normWeight, normHeight, normMUAC]];
   ```

4. **Execute Inference:** Allocate an output tensor buffer and run prediction.

   ```dart
   var outputTensor = List.filled(1 * 3, 0.0).reshape([1, 3]);
   interpreter.run(inputTensor, outputTensor);
   ```

5. **Update UI:** Parse class probabilities to render status labels (e.g., Normal, MAM, SAM).

---

## API-Based vs. On-Device Inference

| Feature / Metric | API-Based Prediction | TensorFlow Lite On-Device Prediction |
| --- | --- | --- |
| **Internet Dependency** | Requires active connection | **100% Offline functional** |
| **Prediction Latency** | High (100–1000ms network roundtrip) | **Ultra-low (5–50ms execution)** |
| **Data Privacy** | Transmits patient data over web | **High privacy (data stays on phone)** |
| **Server Cost** | Recurring cloud hosting costs | **Zero cloud server expense** |
| **App Size** | Small app bundle | Larger app size (includes model weight file) |
| **Model Updates** | Real-time on server | Requires app updates or asset download |

---

## Advantages and Limitations

### Advantages

- **Offline Functionality:** Works seamlessly in off-grid rural areas with zero cellular or Wi-Fi coverage.
- **Instant Triage Results:** Provides instant risk assessment in low-latency clinical environments.
- **Enhanced Privacy & Compliance:** Patient records remain on the local hardware, mitigating data-leak risks.
- **Zero Operating Costs:** Avoids per-request cloud API and server infrastructure fees.

### Limitations

- **Increased Application Footprint:** Adding `.tflite` models increases overall APK/IPA package size.
- **Hardware Limitations:** Constrained by the mobile device's local memory (RAM) and processing power.
- **Update Friction:** Updating model weights requires rolling out a new app release or an over-the-air file update.

---

## Child Malnutrition Application Use Case

In field health settings, healthcare practitioners require immediate diagnostic support to detect child malnutrition early.

### Application Workflow

1. **User Input:** A health worker enters:
   - Child Age (months)
   - Weight (kg)
   - Height / Length (cm)
   - Gender
   - Mother's Education
   - Household Wealth
2. **Local Processing:** Flutter normalizes variables against WHO growth standard baseline figures.
3. **Model Prediction:** The `.tflite` model evaluates inputs and calculates risk probabilities.
4. **Clinical Output:** The app renders color-coded indicators:
   - 🟢 **Green (Normal):** Routine dietary counseling and scheduled monitoring.
   - 🟡 **Yellow (Moderate Acute Malnutrition - MAM):** Supplementary feeding recommendations.
   - 🔴 **Red (Severe Acute Malnutrition - SAM):** Immediate referral to therapeutic care centers.
