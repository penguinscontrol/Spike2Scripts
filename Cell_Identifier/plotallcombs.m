function plotallcombs(x)
cd('C:\Users\The Doctor\Documents\GitHub\Spike2Scripts\Cell_Identifier\');
plotfeats(x,'wid','isi_kurt');
plotfeats(x,'wid','isi_skew');
plotfeats(x,'wid','isi_med');
plotfeats(x,'wid','isi_cv');
plotfeats(x,'wid','med_cv2');
plotfeats(x,'wid','depth');

plotfeats(x,'isi_kurt','isi_skew');
plotfeats(x,'isi_kurt','isi_med');
plotfeats(x,'isi_kurt','isi_cv');
plotfeats(x,'isi_kurt','med_cv2');
plotfeats(x,'isi_kurt','depth');

plotfeats(x,'isi_skew','isi_med');
plotfeats(x,'isi_skew','isi_cv');
plotfeats(x,'isi_skew','med_cv2');
plotfeats(x,'isi_skew','depth');

plotfeats(x,'isi_med','isi_cv');
plotfeats(x,'isi_med','med_cv2');
plotfeats(x,'isi_med','depth');

plotfeats(x,'isi_cv','med_cv2');
plotfeats(x,'isi_cv','depth');

plotfeats(x,'med_cv2','depth');
end