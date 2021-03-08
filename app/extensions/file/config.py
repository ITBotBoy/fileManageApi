# 文件相关配置
FILE = {
    "STORE_DIR": 'app/assets',
    'img':{
        "SINGLE_LIMIT": 1024 * 1024 * 10,
        "TOTAL_LIMIT": 1024 * 1024 * 10,
        "NUMS": 10,
        "INCLUDE": set([]),
        "EXCLUDE": set([])
    },
    'txt':{
        "SINGLE_LIMIT": 1024 * 1024 * 100,
        "TOTAL_LIMIT": 1024 * 1024 * 100,
        "NUMS": 10,
        "INCLUDE": set([]),
        "EXCLUDE": set([])
    },
    'video':{
        "SINGLE_LIMIT": 1024 * 1024 * 1024 * 3,
        "TOTAL_LIMIT": 1024 * 1024 * 1024 * 3,
        "NUMS": 10,
        "INCLUDE": set([]),
        "EXCLUDE": set([])
    },
    'audio':{
        "SINGLE_LIMIT": 1024 * 1024 * 1024,
        "TOTAL_LIMIT": 1024 * 1024 * 1024,
        "NUMS": 10,
        "INCLUDE": set([]),
        "EXCLUDE": set([])
    }
}
