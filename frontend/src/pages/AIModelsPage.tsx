import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { AIModelStatus } from '../types';
import {
  Cpu,
  Layers,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Code2,
  Terminal,
  Activity
} from 'lucide-react';

export const AIModelsPage: React.FC = () => {
  const [models, setModels] = useState<AIModelStatus[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    apiClient.getAiModelsStatus().then((data) => {
      setModels(data);
      setLoading(false);
    }).catch(console.error);
  }, []);

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-50 text-purple-600 rounded-lg">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>Modular AI/ML Architecture & Model Registry</span>
              <span className="text-xs font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                PyTorch & Scikit-Learn Interfaces
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Decoupled abstract base models supporting Siamese CNNs, SegFormer transformers, and explainable risk engines.
            </p>
          </div>
        </div>
      </div>

      {/* Model Spec Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {models.map((m, idx) => (
          <div key={idx} className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
            <div className="flex items-start justify-between gap-2">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                  {m.module}
                </span>
                <h3 className="font-bold text-sm text-slate-900 mt-1">{m.active_model}</h3>
              </div>
              <span className="text-[11px] font-mono font-semibold px-2 py-0.5 bg-slate-100 text-slate-700 rounded border border-slate-200">
                {m.inference_latency_ms} ms
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-50 p-2 rounded border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-400">Architecture</span>
                <div className="font-semibold text-slate-800">{m.model_type}</div>
              </div>
              <div className="bg-slate-50 p-2 rounded border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-400">Input Tensor</span>
                <div className="font-mono text-slate-800 text-[11px] truncate">{m.input_shape}</div>
              </div>
            </div>

            <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200 text-xs">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-1">
                Benchmark Metric & Validation
              </span>
              <div className="font-mono font-bold text-slate-900">
                {m.f1_score || m.mIoU || m.explainability || m.direction_accuracy}
              </div>
            </div>

            <div className="text-[11px] text-slate-500">
              <span className="font-bold text-slate-700">Supported Alternatives:</span>{' '}
              {m.supported_alternatives.join(', ')}
            </div>
          </div>
        ))}
      </div>

      {/* Code Integration Example */}
      <div className="bg-slate-900 text-slate-200 rounded-xl border border-slate-800 p-4 space-y-3 font-mono text-xs shadow-md">
        <div className="flex items-center justify-between pb-2 border-b border-slate-800">
          <div className="flex items-center gap-2 text-slate-300 font-bold">
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span>How to Load Pretrained PyTorch Weights (Drop-in Replacement)</span>
          </div>
          <span className="text-slate-500 text-[11px]">app/ai/change_detection.py</span>
        </div>

        <pre className="text-slate-300 overflow-x-auto leading-relaxed bg-slate-950/80 p-3 rounded-lg border border-slate-800">
{`from app.ai.base_models import BaseChangeDetectionModel
import torch

class CustomSiameseResNetModel(BaseChangeDetectionModel):
    def __init__(self, checkpoint_path="weights/siamese_imd_v1.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(checkpoint_path, map_location=self.device)
        self.model.eval()

    def detect_change(self, t1_features, t2_features, **kwargs):
        # 1. Convert optical & SAR rasters to torch tensor [B, C=12, H, W]
        # 2. Forward pass through Siamese backbone
        # 3. Apply sigmoid thresholding for change mask
        return {
            "model_used": "PyTorch Siamese ResNet-34",
            "model_status": "Trained Production Model",
            "change_percentage": 91.2,
            "changed_area_hectares": 14.2
        }`}
        </pre>
      </div>
    </div>
  );
};
