import pandas as pd, numpy as np, joblib, json
from sklearn.model_selection import KFold, cross_validate, GroupShuffleSplit, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.inspection import permutation_importance

df = pd.read_csv('/mnt/user-data/uploads/auto-mpg.csv')
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')   # '?' -> NaN
print('missing hp rows:', df['horsepower'].isna().sum())
df['l100'] = 235.215 / df['mpg']          # US mpg -> L/100 km
df['year'] = df['model year'] + 1900
num = ['cylinders','displacement','horsepower','weight','acceleration','year']
print(df[['l100']+num].describe().round(2))
print(df[['l100']+num+['origin']].corr(method='spearman')['l100'].round(3))
print(df.groupby('origin')['l100'].agg(['count','mean']).round(2))
print(df.groupby('cylinders')['l100'].agg(['count','mean']).round(2))
print(df.groupby('year')['l100'].mean().round(2).to_dict())

X = df[num+['origin']]; y = df['l100']
groups = df['car name']
cat = ['origin']
def prep(scale=True):
    return ColumnTransformer([('c', OneHotEncoder(drop='first'), cat)],
        remainder=StandardScaler() if scale else 'passthrough')
from sklearn.impute import SimpleImputer
def pipe(model, scale=True):
    return make_pipeline(ColumnTransformer([
        ('n', make_pipeline(SimpleImputer(strategy='median'), StandardScaler() if scale else 'passthrough'), num),
        ('c', OneHotEncoder(drop='first'), cat)]), model)

# hold-out split grouped by car name (no same-name car in train and test)
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
tr, te = next(gss.split(X, y, groups))
Xtr, Xte, ytr, yte = X.iloc[tr], X.iloc[te], y.iloc[tr], y.iloc[te]
print('train/test', len(tr), len(te))

models = {
 'Baseline (mean)': pipe(DummyRegressor()),
 'Linear regression': pipe(LinearRegression()),
 'Ridge': pipe(RidgeCV(alphas=np.logspace(-3,3,30))),
 'Random forest': pipe(RandomForestRegressor(500, min_samples_leaf=2, random_state=0, n_jobs=-1), False),
 'Gradient boosting': pipe(GradientBoostingRegressor(n_estimators=300, learning_rate=0.03, max_depth=3, subsample=0.8, random_state=0), False),
}
cv = KFold(5, shuffle=True, random_state=1)
rows=[]
for n,m in models.items():
    s = cross_validate(m, Xtr, ytr, cv=cv, scoring=('neg_mean_absolute_error','neg_root_mean_squared_error','r2'))
    rows.append((n, -s['test_neg_mean_absolute_error'].mean(), -s['test_neg_root_mean_squared_error'].mean(), s['test_r2'].mean()))
cvres = pd.DataFrame(rows, columns=['model','CV MAE','CV RMSE','CV R2']).round(3)
print(cvres)

# also an ablation: weight only
wm = make_pipeline(LinearRegression()).fit(Xtr[['weight']], ytr)
print('weight-only linear test R2', round(r2_score(yte, wm.predict(Xte[['weight']])),3),
      'MAE', round(mean_absolute_error(yte, wm.predict(Xte[['weight']])),3))

# tune GB lightly
gs = GridSearchCV(pipe(GradientBoostingRegressor(subsample=0.8, random_state=0), False),
    {'gradientboostingregressor__n_estimators':[200,400],'gradientboostingregressor__learning_rate':[0.02,0.05],
     'gradientboostingregressor__max_depth':[2,3,4]}, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1).fit(Xtr,ytr)
print('GB best', gs.best_params_, round(-gs.best_score_,3))

res=[]
final = {'Ridge':models['Ridge'],'Random forest':models['Random forest'],'Gradient boosting (tuned)':gs.best_estimator_,'Baseline (mean)':models['Baseline (mean)']}
for n,m in final.items():
    m.fit(Xtr,ytr); p=m.predict(Xte)
    res.append((n, mean_absolute_error(yte,p), mean_squared_error(yte,p)**.5, r2_score(yte,p)))
    if n.startswith('Gradient'): pg=p
print(pd.DataFrame(res,columns=['model','test MAE','test RMSE','test R2']).round(3))
print('GB test MAE % of mean', round(100*mean_absolute_error(yte,pg)/yte.mean(),1))
print('abs err 90th pct', np.percentile(np.abs(yte-pg),90).round(2))
# residuals by group
r = pd.DataFrame({'y':yte,'p':pg,'origin':Xte['origin']}); r['e']=(r.y-r.p)
print(r.groupby('origin')['e'].agg(lambda e: np.abs(e).mean()).round(2))
print('bias', r.e.mean().round(3))
# importance
pi = permutation_importance(gs.best_estimator_, Xte, yte, n_repeats=30, random_state=0, scoring='neg_mean_absolute_error')
print(pd.Series(pi.importances_mean, index=X.columns).sort_values(ascending=False).round(3))
# ridge coefs
rid = models['Ridge']; print(dict(zip(num, rid[-1].coef_[:6].round(3))))
# final model on all data
best = gs.best_estimator_.fit(X,y)
joblib.dump(best,'fuel_model.joblib')
print('saved')
