from fastapi import APIRouter, HTTPException
import httpx


router = APIRouter(prefix="/widgets/github")

def fetch_github(username: str):
    url = f"https://api.github.com/users/{username}"
    try:
        # get profile
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub user not found")
        
        response.raise_for_status()
        data = response.json()

        # get recent repos
        repos_response = httpx.get(f"https://api.github.com/users/{username}/repos", params={"sort": "updated", "per_page": 3}, timeout=5.0)
        repos_response.raise_for_status()
        repos_data = repos_response.json()


    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="GitHub service is unavailable")
    
    
    
    repos = []
    for repo in repos_data:
            repos.append({
                "name": repo["name"],
                "language": repo["language"],
                "stars": repo["stargazers_count"],
                "url": repo["html_url"]
            })

    return {
        "username": data["login"],
        "avatar_url": data["avatar_url"],
        "public_repos": data["public_repos"],
        "followers": data["followers"],
        "profile_url": data["html_url"],
        "recent_repos": repos

    }

@router.get("/")
def get_github(username: str):
    return fetch_github(username)