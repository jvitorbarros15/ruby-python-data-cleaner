Rails.application.routes.draw do
  root "pages#home"
  get "pages/home"

  # DATA ROUTES
  get "/data", to: "data#index"
  get "/data/show", to: "data#show"    # <--- ADD THIS
  post "/data/run", to: "data#run"     # runs python scripts

  # Health check
  get "up" => "rails/health#show", as: :rails_health_check
end
