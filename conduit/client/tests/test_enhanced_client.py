#!/usr/bin/env python3

import sys

from conduit.client.base import DEFAULT_USER_AGENT
from conduit.client.unified import (
    ClientConfig,
    EnhancedPhabricatorClient,
    PhabricatorClient,
)


def test_basic_client():
    """Test basic client functionality (backward compatibility)."""
    print("Testing basic client...")

    # Test basic client creation (should use original configuration)
    client = PhabricatorClient(
        api_url="https://test.example.com/api/", api_token="test_token"
    )

    # Check that it's a basic client
    stats = client.get_stats()
    print(f"Basic client stats: {stats}")
    assert "Basic client - no enhanced features enabled" in stats["message"]

    # Test that all modules are initialized
    assert hasattr(client, "maniphest")
    assert hasattr(client, "differential")
    assert hasattr(client, "diffusion")
    assert hasattr(client, "project")
    assert hasattr(client, "user")
    assert hasattr(client, "file")
    assert hasattr(client, "conduit")
    assert hasattr(client, "harbormaster")
    assert hasattr(client, "paste")
    assert hasattr(client, "phriction")
    assert hasattr(client, "remarkup")
    assert hasattr(client, "macro")
    assert hasattr(client, "flag")
    assert hasattr(client, "phid")

    client.close()
    print("✓ Basic client test passed")


def test_enhanced_client():
    """Test enhanced client functionality."""
    print("\nTesting enhanced client...")

    # Test enhanced client creation
    client = PhabricatorClient(
        api_url="https://test.example.com/api/",
        api_token="test_token",
        timeout=60.0,
        max_retries=5,
        enable_cache=True,
        connect_timeout=15.0,
        read_timeout=45.0,
        write_timeout=45.0,
        retry_delay=2.0,
        retry_backoff=1.5,
        cache_ttl=600,
    )

    # Check that it's an enhanced client
    stats = client.get_stats()
    print(f"Enhanced client stats: {stats}")

    # Verify enhanced features are enabled
    assert "config" in stats
    assert stats["config"]["timeout"] == 60.0
    assert stats["config"]["max_retries"] == 5
    assert stats["config"]["enable_cache"] is True
    assert stats["config"]["cache_ttl"] == 600
    assert stats["cache_size"] == 0  # Initially empty
    assert "connection_pool" in stats

    # Test cache clearing
    client.clear_cache()
    print("✓ Cache clearing test passed")

    client.close()
    print("✓ Enhanced client test passed")


def test_client_config():
    """Test ClientConfig class."""
    print("\nTesting ClientConfig...")

    # Test default configuration
    config = ClientConfig()
    assert config.timeout == 30.0
    assert config.connect_timeout == 10.0
    assert config.read_timeout == 30.0
    assert config.write_timeout == 30.0
    assert config.max_retries == 3
    assert config.retry_delay == 1.0
    assert config.retry_backoff == 2.0
    assert config.enable_cache is True
    assert config.cache_ttl == 300

    # Test custom configuration
    config = ClientConfig(
        timeout=60.0, max_retries=5, enable_cache=False, custom_param="test_value"
    )
    assert config.timeout == 60.0
    assert config.max_retries == 5
    assert config.enable_cache is False
    assert config.extra_config["custom_param"] == "test_value"

    print("✓ ClientConfig test passed")


def test_enhanced_direct():
    """Test direct EnhancedPhabricatorClient usage."""
    print("\nTesting direct EnhancedPhabricatorClient...")

    # Test direct enhanced client creation
    enhanced_client = EnhancedPhabricatorClient(
        api_url="https://test.example.com/api/",
        api_token="test_token",
        timeout=45.0,
        max_retries=2,
        enable_cache=True,
    )

    # Check enhanced client specific methods
    stats = enhanced_client.get_stats()
    print(f"Direct enhanced client stats: {stats}")

    # Test that it has the request method
    assert hasattr(enhanced_client, "request")

    enhanced_client.close()
    print("✓ Direct EnhancedPhabricatorClient test passed")


def test_user_agent_default():
    """The default User-Agent is applied when no override is passed."""
    print("\nTesting default User-Agent...")

    # Basic (non-enhanced) path
    basic = PhabricatorClient(
        api_url="https://test.example.com/api/", api_token="test_token"
    )
    assert basic.http_client.headers["user-agent"] == DEFAULT_USER_AGENT
    basic.close()

    # Enhanced path (triggered by non-default timeout)
    enhanced = PhabricatorClient(
        api_url="https://test.example.com/api/",
        api_token="test_token",
        timeout=60.0,
    )
    assert enhanced.http_client.headers["user-agent"] == DEFAULT_USER_AGENT
    enhanced.close()

    # Direct EnhancedPhabricatorClient
    direct = EnhancedPhabricatorClient(
        api_url="https://test.example.com/api/", api_token="test_token"
    )
    assert direct.http_client.headers["user-agent"] == DEFAULT_USER_AGENT
    direct.close()

    print("✓ Default User-Agent test passed")


def test_user_agent_override():
    """A user_agent kwarg overrides the default in all client flavors."""
    print("\nTesting User-Agent override...")

    custom_ua = "MyOrg-Phabricator-MCP/1.0 (contact@example.org)"

    # Basic (non-enhanced) path
    basic = PhabricatorClient(
        api_url="https://test.example.com/api/",
        api_token="test_token",
        user_agent=custom_ua,
    )
    assert basic.http_client.headers["user-agent"] == custom_ua
    basic.close()

    # Enhanced path via PhabricatorClient wrapper
    enhanced = PhabricatorClient(
        api_url="https://test.example.com/api/",
        api_token="test_token",
        timeout=60.0,
        user_agent=custom_ua,
    )
    assert enhanced.http_client.headers["user-agent"] == custom_ua
    enhanced.close()

    # Direct EnhancedPhabricatorClient
    direct = EnhancedPhabricatorClient(
        api_url="https://test.example.com/api/",
        api_token="test_token",
        user_agent=custom_ua,
    )
    assert direct.http_client.headers["user-agent"] == custom_ua
    direct.close()

    print("✓ User-Agent override test passed")


if __name__ == "__main__":
    print("Running enhanced client tests...")

    try:
        test_client_config()
        test_basic_client()
        test_enhanced_client()
        test_enhanced_direct()
        test_user_agent_default()
        test_user_agent_override()

        print("\nAll tests passed successfully!")

    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
